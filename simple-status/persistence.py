import asyncio

COMPONENTS = {}
COMPONENTS_LOCK = asyncio.Lock()
CONFIGS = {}
CONFIGS_LOCK = asyncio.Lock()
STATUSES = {}
STATUSES_LOCK = asyncio.Lock()
MODIFIED = False
MODIFIED_LOCK = asyncio.Lock()