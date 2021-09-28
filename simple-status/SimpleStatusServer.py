# for recursive definitions
from __future__ import annotations

import json
import logging
from logging.config import fileConfig
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
# from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse

import persistence
from models import ConfigIn, ConfigStored, StatusIn, ComponentStatusOut, ComponentTimeoutConfig
from persistence import COMPONENTS, COMPONENTS_LOCK, CONFIGS_LOCK, STATUSES_LOCK, MODIFIED_LOCK
import dotenv
from os import environ


dotenv.load_dotenv(".env")

# LOGGING_PATH=environ["LOGGING_PATH"]

PORT=int(environ["PORT"])
STATIC_PATH=environ["STATIC_PATH"]
SWAGGER_STATIC_PATH=environ["SWAGGER_STATIC_PATH"]
LOGGING_CONFIG_INI =environ["LOGGING_CONFIG_INI"]
#if DEBUG is present, we are debugging
try:
    environ["DEBUG"]
    DEBUG=True
except:
    DEBUG=False


def main():
    api_app = FastAPI(title="api", docs_url=None, redoc_url=None, debug=DEBUG)
    app = FastAPI(title="main", docs_url=None, redoc_url=None, debug=DEBUG)
    # origins = ["http://localhost", "http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000",
    # "http://127.0.0.1:3001"]
    origins = ["*"]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                       allow_headers=["*"])

    async def add_component(component_key, parent_key, parent_chain=None):
        logger_back.info(f"add_component")
        logger_back.debug(f"add_component {component_key} {parent_key} {parent_chain}")
        if not parent_chain:
            parent_chain = list()
        async with COMPONENTS_LOCK:
            # add a component with an updated chain
            if parent_key:
                persistence.COMPONENTS[component_key] = parent_chain + [parent_key]
            else:
                persistence.COMPONENTS[component_key] = parent_chain
            async with MODIFIED_LOCK:
                persistence.MODIFIED = True

    @api_app.post("/components/{component_key}/config")
    async def set_config(component_key: int, config: ConfigIn):
        logger_back.info(f"add_component")
        logger_back.debug(f"add_component {component_key} {config}")
        config_dict = json.loads(config.json())
        if config.parent_key:
            logger_back.info(f"storing config with parent {config.parent_key}")
            try:
                parent_chain = COMPONENTS[config.parent_key]
            except KeyError:
                logging.error("parent component not found, your parent component needs to have sent it's config prior to you sending yours")
                raise HTTPException(status_code=404,
                                    detail="parent component not found, your parent component needs to have sent it's "
                                           "config prior to you sending yours")
            # walk down from the top of the configs to get to where we want to insert our config
            parent = None
            async with CONFIGS_LOCK:
                #validate parent_chain
                if parent_chain:
                    logger_back.info("validating config chain")
                    current_config: ConfigStored = persistence.CONFIGS[parent_chain[0]]
                    for key in parent_chain[1:] + [config.parent_key]:
                        logger_back.debug(f"current config is {current_config}")
                        try:
                            current_config = current_config.subcomponents[key]
                        except KeyError as _:
                            logging.exception(
                                f"fthis should not happen, it means your parent chain was corrupted as we were not "
                                f"able "
                                f"to find a config for one of your parents: original {component_key}, parent_chain "
                                f"{parent_chain}, failed on {current_config}")
                            raise HTTPException(
                                "An error occurred due to data corruption, please contact the developer.  Further "
                                "information in server logs")
                else:
                    current_config: ConfigStored = persistence.CONFIGS[config.parent_key]
                # ok we have where we want to insert our new config
                stored_config = ConfigStored(**config_dict, key=component_key)
                # if we already have a config we don't want to lose the subcomponents
                if component_key in current_config.subcomponents:
                    stored_config.subcomponents = current_config.subcomponents[component_key].subcomponents
                else:
                    current_config.subcomponents[component_key] = stored_config
                parent = current_config.name
                await add_component(component_key, config.parent_key, parent_chain)
        else:
            logger_back.info(f"storing config with no parent")
            parent = "None"
            parent_key = 0
            config_dict["parent_key"] = parent_key
            await add_component(component_key, parent_key)
            stored_config = ConfigStored(**config_dict, key=component_key)
            async with CONFIGS_LOCK:
                persistence.CONFIGS[component_key] = stored_config
        return {"config": stored_config, "parent": parent}

    @api_app.post("/components/{component_key}/status")
    async def set_status(component_key: int, status: StatusIn):
        # json_status = jsonable_encoder(status)
        logger_back.info(f"set_status")
        logger_back.debug(f"set_status {component_key} {status}")
        async with CONFIGS_LOCK:
            try:
                persistence.CONFIGS[component_key]
            except KeyError:
                logger_back.warning(f"There is no configuration for that key, you must have a configuration for that key in order to send a status for it")
                raise HTTPException(status_code=404,
                                    detail="There is no configuration for that key, you must have a configuration for "
                                           "that key in order to send a status for it")
        async with STATUSES_LOCK:
            status_list = persistence.STATUSES[component_key]
            status_list.append(status)
            async with MODIFIED_LOCK:
                persistence.MODIFIED = True
        return {"component_key": component_key, "status": status}

    @api_app.get("/components/statuses", response_model=List[ComponentStatusOut])
    async def get_statuses():
        logger_back.info(f"get_statuses")
        async with STATUSES_LOCK as a, CONFIGS_LOCK as b:
            return await parse_configs_for_statuses(persistence.CONFIGS.values())

    async def parse_configs_for_statuses(configs):
        logger_back.info(f"parse_configs_for_statuses")
        logger_back.debug(f"parse_configs_for_statuses {configs}")
        built_statuses = []
        for config in configs:
            logger_back.debug(f"parsing {config}")
            status_list = persistence.STATUSES[config.key]
            logger_back.debug(f"got statuses {status_list}")
            if not status_list:
                return []
            status = status_list[-1]
            built_status = await  build_status(config, status)
            substatuses = await parse_configs_for_statuses(config.subcomponents.values())
            built_status.subcomponents = substatuses
            built_statuses.append(built_status)
        return built_statuses

    async def build_status(config: ConfigStored, status: StatusIn):
        logger_back.info(f"build_status")
        logger_back.debug(f"build_status {config} {status}")
        timeout_config = ComponentTimeoutConfig(timeout_min=config.timeout_min, timeout_color=config.timeout_color)
        component_status = ComponentStatusOut(name=config.name, details=config.details, date=status.date,
                                              status=status.color, config=timeout_config, status_message=status.message,
                                              key=config.key)
        return component_status

    @api_app.get("/ping")
    def pong():
        logger_back.info("ping")
        return {"ping": "pong!"}


    @api_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            # openapi_url=api_app.openapi_url,
            openapi_url="/api" + api_app.openapi_url,
            title=api_app.title + " - Swagger UI",
            oauth2_redirect_url=api_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/api/static/swagger-ui-bundle.js",
            swagger_css_url="/api/static/swagger-ui.css",
        )

    @api_app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @api_app.get("/redoc", include_in_schema=False)
    async def redoc_html(request: Request):
        return get_redoc_html(
            openapi_url="/api" + api_app.openapi_url,
            title=api_app.title + " - ReDoc",
            redoc_js_url="/api/static/redoc.standalone.js",
        )

    api_app.mount("/static", StaticFiles(directory=SWAGGER_STATIC_PATH), name='swagger')
    app.mount("/api", api_app)

    app.mount("/", StaticFiles(directory=STATIC_PATH, html=True), name="static")

    return app


if __name__ == "__main__":
    #setup logging from file
    fileConfig(LOGGING_CONFIG_INI)
    logger_front = logging.getLogger("SSFront")
    logger_back = logging.getLogger("SSBack")
    import uvicorn

    app = main()

    uvicorn.run(app, host="0.0.0.0", port=PORT)
