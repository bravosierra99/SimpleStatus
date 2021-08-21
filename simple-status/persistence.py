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