import asyncio
from collections import defaultdict

# these global objects will represent my current datastore... you could switch to something more databasey in the future
COMPONENTS = {}
COMPONENTS_LOCK = asyncio.Lock()
CONFIGS = {}
CONFIGS_LOCK = asyncio.Lock()
STATUSES = defaultdict(list)
STATUSES_LOCK = asyncio.Lock()
MODIFIED = False
MODIFIED_LOCK = asyncio.Lock()

import logging
logger_back = logging.getLogger("SSBack")

class PersistenceError(Exception):
    pass

async def retrieve_config(component_key:int):
    async with CONFIGS_LOCK:
        try:
            async with COMPONENTS_LOCK:
                parent_chain = COMPONENTS[component_key]
            if parent_chain:
                current_config = CONFIGS[parent_chain[0]]
                #already grabbed first config
                parent_chain = parent_chain[1:]
                #matching config not in parent_chain
                parent_chain.append(component_key)
                for key in parent_chain:
                    current_config = current_config.subcomponents[key]
            else:
                current_config = CONFIGS[component_key]
        except KeyError as e:
            logger_back.warning(
                f"There is no configuration for that key, you must have a configuration for that key in order "
                f"to "
                f"send a status for it")
            logger_back.debug(f"components: {COMPONENTS}")
            logger_back.debug(f"configs: {CONFIGS}")
            logger_back.error(str(e))
            raise PersistenceError("There is no configuration for that key, you must have a configuration for that key in order to send a status for it")
        return  current_config



