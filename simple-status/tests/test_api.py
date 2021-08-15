
import pytest
import requests
import asyncio
import yarl
import pathlib

CONFIG = 'config'

COMPONENTS = "components"


def test_set_config_single(test_app):
    component_key = 1
    url = yarl.URL(COMPONENTS) / str(component_key) / CONFIG
    first = {
        "name": "first",
        "parent_key": 0,
        "details": "first details",
        "timeout_min": 0,
        "timeout_color": "green"
    }
    result : requests.Response = test_app.post(str(url),json=first)
    assert result.status_code == 200
    assert result.json()["config"]["key"] == component_key


