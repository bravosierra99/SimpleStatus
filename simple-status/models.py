from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional, List

from fastapi import Body
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

class ComponentTimeoutConfig(BaseModel):
    timeout_min: int
    timeout_color: Colors

class ComponentStatusOut(BaseModel):
    name: str
    details: str
    date: datetime
    status: Colors
    config: ComponentTimeoutConfig
    status_message: str
    key: int
    subcomponents: List[ComponentStatusOut] =  Body([])

    class Config:
        allow_mutation : True
ComponentStatusOut.update_forward_refs()
# ComponentStatus.__pydantic_model__.update_forward_refs()
# class ComponentStatusesOut(BaseModel):
#     statuses: Optional[List[ComponentStatus]] = []



class StatusIn(BaseModel):
    color: Colors
    date: datetime
    message: str