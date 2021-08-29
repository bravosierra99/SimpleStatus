import pytest
from starlette.testclient import TestClient

from SimpleStatusServer import frontend_app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(frontend_app)
    yield client  # testing happens here