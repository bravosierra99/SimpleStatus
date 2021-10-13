import json
from datetime import datetime, timedelta

import requests
import yarl
from models import Colors, StatusIn, ComponentStatusOut
from pydantic import parse_raw_as

STATUSES = "statuses"
STATUS = "status"

CONFIG = 'config'

COMPONENTS = "components"



def test_set_config_single(test_app, api_url):
    component_key = 1
    url = yarl.URL(api_url) / COMPONENTS / str(component_key) / CONFIG
    first = {
        "name": "first",
        "parent_key": 0,
        "details": "first details",
        "timeout_min": 0,
        "timeout_color": "green"
    }
    result: requests.Response = test_app.post(str(url), json=first)
    assert result.status_code == 200
    assert result.json()["config"]["key"] == component_key


def test_set_status_single(test_app, api_url):
    setup_some_configs(test_app, api_url)
    component_key = 1
    set_status_url = yarl.URL(api_url) / COMPONENTS / str(component_key) / STATUS
    status_json = {
        "color": Colors.green.name,
        "date": datetime.now().isoformat(),
        "message": "everything is awesome"
    }
    result = test_app.post(str(set_status_url), json=status_json)
    assert result.status_code == 200
    json_result = result.json()
    assert json_result['component_key'] == component_key
    assert json_result['status'] == status_json


def test_get_statuses(test_app, api_url):
    setup_some_configs(test_app, api_url)
    setup_some_statuses(test_app, api_url)


    # ok now that we have statuses let's check to make sure they look correct
    get_status_url = yarl.URL(api_url) / COMPONENTS / STATUSES
    result: requests.Response = test_app.get(str(get_status_url))
    assert result.status_code == 200
    statuses = json.loads(result.content)
    statuses = [ComponentStatusOut(**status) for status in statuses]
    print(statuses)



def setup_some_statuses(test_app, api_url):
    # ok first we need to build up some configs
    params = [
        [1, Colors.green.name, datetime.now().isoformat(), "Everything is awesome"],
        [2, Colors.yellow.name, (datetime.now() - timedelta(hours=10)).isoformat(), "only partially completed"],
        [12, Colors.green.name, (datetime.now() - timedelta(hours=12)).isoformat(), "Everything is awesome"],
        [123, Colors.red.name, (datetime.now() - timedelta(hours=5)).isoformat(), "The Cake is a lie"],
    ]
    for param in params:
        component_key = param[0]
        status = StatusIn(color=param[1], date=param[2], message=param[3])

        url = yarl.URL(api_url) / COMPONENTS / str(component_key) / STATUS

        status_json = json.loads(status.json())
        result: requests.Response = test_app.post(str(url), json=status_json)
        json_result = result.json()
        assert result.status_code == 200
        assert json_result['component_key'] == component_key
        assert json_result['status'] == status_json


def setup_some_configs(test_app, api_url):
    # ok first we need to build up some configs
    params = [
        [1, "first", 0, "first details", 1, "yellow"],
        [2, "second", 0, "second details", 1, "yellow"],
        [12, "first second", 1, "first second details", 100, "yellow"],
        [123, "first second third", 12, "first second third details", 200, "red"],
    ]
    for param in params:
        component_key = param[0]
        json_config = {
            "name": param[1],
            "parent_key": param[2],
            "details": param[3],
            "timeout_min": param[4],
            "timeout_color": param[5]
        }
        url = yarl.URL(api_url) / COMPONENTS / str(component_key) / CONFIG

        result: requests.Response = test_app.post(str(url), json=json_config)
        assert result.status_code == 200
        assert result.json()["config"]["key"] == component_key
    return json_config
