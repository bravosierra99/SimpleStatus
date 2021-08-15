# for recursive definitions
from __future__ import annotations

import json
import logging

from fastapi import FastAPI, HTTPException

import persistence
from models import ConfigIn, ConfigStored, StatusIn
from persistence import COMPONENTS, COMPONENTS_LOCK, CONFIGS_LOCK, STATUSES_LOCK, MODIFIED_LOCK

logging.basicConfig(filename=r"D:\Users\ben\Documents\telework\SimpleStatus\simple-status\files\SimpleStatusServer.log", level=logging.DEBUG)

app = FastAPI()

# these global objects will represent my current datastore... you could switch to something more databasey in the future

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


@app.post("/components/{component_key}/config")
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





@app.post("/components/{component_key}/status")
async def set_status(component_key: int, status: StatusIn):
    async with STATUSES_LOCK:
        persistence.STATUSES.get(component_key, list).append(status)
        async with MODIFIED_LOCK:
            persistence.MODIFIED = True

    return {"component_key": component_key, "status": status}


@app.get("/components/status")
async def get_statuses(response_model=None):
    pass

@app.get("/ping")
def pong():
    return {"ping": "pong!"}

#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#
#     return {"model_name": model_name, "message": "Have some residuals"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
