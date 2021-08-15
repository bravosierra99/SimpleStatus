from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Colors(Enum):
    green = "green"
    yellow = "yellow"
    red = "red"


class ConfigIn(BaseModel):
    name: str
    parent_key: Optional[int]
    details: str
    timeout_min: int
    timeout_color: Colors


class ConfigStored(BaseModel):
    key: int
    name: str
    parent_key: Optional[int]
    details: str
    timeout_min: int
    timeout_color: Colors
    subcomponents: dict = dict()


class StatusIn(BaseModel):
    color: Colors
    date: datetime
    message: str