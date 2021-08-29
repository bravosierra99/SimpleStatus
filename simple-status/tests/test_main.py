from starlette.testclient import TestClient

from SimpleStatusServer import frontend_app



def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}