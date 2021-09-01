# for recursive definitions
from __future__ import annotations

import json
import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse

import persistence
from models import ConfigIn, ConfigStored, StatusIn, ComponentStatusOut, ComponentTimeoutConfig
from persistence import COMPONENTS, COMPONENTS_LOCK, CONFIGS_LOCK, STATUSES_LOCK, MODIFIED_LOCK
import dotenv
from os import environ

dotenv.load_dotenv(".env")

LOGGING_PATH=environ["LOGGING_PATH"]
PORT=environ["PORT"]
STATIC_PATH=environ["STATIC_PATH"]


logging.basicConfig(filename=LOGGING_PATH,
                    level=logging.DEBUG)

frontend_app = FastAPI()
api_app = FastAPI()
app = FastAPI()
# origins = ["http://localhost", "http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000","http://127.0.0.1:3001"]
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


async def add_component(component_key, parent_key, parent_chain=None):
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
    config_dict = json.loads(config.json())
    if config.parent_key:
        try:
            parent_chain = COMPONENTS[config.parent_key]
        except KeyError:
            raise HTTPException(status_code=404,
                                detail="parent component not found, your parent component needs to have sent it's "
                                       "config prior to you sending yours")
        # walk down from the top of the configs to get to where we want to insert our config
        parent = None
        async with CONFIGS_LOCK:
            if parent_chain:
                current_config: ConfigStored = persistence.CONFIGS[parent_chain[0]]
                for key in parent_chain[1:] + [config.parent_key]:
                    try:
                        current_config = current_config.subcomponents[key]
                    except KeyError as _:
                        logging.exception(
                            f"fthis should not happen, it means your parent chain was corrupted as we were not able "
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
        parent = "None"
        parent_key = 0
        config_dict["parent_key"] = parent_key
        await add_component(component_key, parent_key)
        stored_config = ConfigStored(**config_dict, key=component_key)
        persistence.CONFIGS[component_key] = stored_config
    return {"config": stored_config, "parent": parent}


@api_app.post("/components/{component_key}/status")
async def set_status(component_key: int, status: StatusIn):
    # json_status = jsonable_encoder(status)
    async with CONFIGS_LOCK:
        try:
            persistence.CONFIGS[component_key]
        except KeyError:
            raise HTTPException(status_code=404,
                                detail="There is no configuration for that key, you must have a configuration for that key in order to send a status for it")
    async with STATUSES_LOCK:
        status_list = persistence.STATUSES[component_key]
        status_list.append(status)
        async with MODIFIED_LOCK:
            persistence.MODIFIED = True
    return {"component_key": component_key, "status": status}


@api_app.get("/components/statuses", response_model=List[ComponentStatusOut])
async def get_statuses():
    async with STATUSES_LOCK as a, CONFIGS_LOCK as b:
        return await parse_configs_for_statuses(persistence.CONFIGS.values())


async def parse_configs_for_statuses(configs):
    built_statuses = []
    for config in configs:
        status_list = persistence.STATUSES[config.key]
        if not status_list:
            return []
        status = status_list[-1]
        built_status = await  build_status(config, status)
        substatuses = await parse_configs_for_statuses(config.subcomponents.values())
        built_status.subcomponents = substatuses
        built_statuses.append(built_status)
    return built_statuses


async def build_status(config: ConfigStored, status: StatusIn):
    timeout_config = ComponentTimeoutConfig(timeout_min=config.timeout_min, timeout_color=config.timeout_color)
    component_status = ComponentStatusOut(name=config.name, details=config.details, date=status.date,
                                          status=status.color, config=timeout_config, status_message=status.message,
                                          key=config.key)
    return component_status


@api_app.get("/ping")
def pong():
    return {"ping": "pong!"}

app.mount("/api", api_app)

@frontend_app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return RedirectResponse("/index.html")
    return response

@frontend_app.exception_handler(404)
def not_found(request, exc):
    return RedirectResponse("/index.html")


frontend_app.mount("/", StaticFiles(directory=STATIC_PATH), name="static")
app.mount("/", frontend_app)
app.mount("/api", api_app)

#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#
#     return {"model_name": model_name, "message": "Have some residuals"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
