import pytest
from starlette.testclient import TestClient

# from dotenv import load_dotenv
# load_dotenv(r"..\.env")

from os import chdir, getcwd
from pathlib import Path
chdir(Path(getcwd()).parent)

from SimpleStatusServer import main


@pytest.fixture(scope="module")
def test_app():
    app = main()
    api_app = None
    for route in app.routes:
        try:
            if route.app.title == "api":
                api_app = route.app
                break
        #only wanted routes for mounted apps
        except:
            pass
    if api_app:
        # #maybe a better way to do this but I don't know how to fully resolve routes
        # def post(self,*args, **kwargs):
        #     self.post(self,"/api/" + args[0],*args[0:], **kwargs )
        # app.post = post
        client = TestClient(app)
        yield client  # testing happens here
    else:
        raise Exception("unable to find api app, looked in root app's first level routes")


@pytest.fixture(scope="module")
def api_url():
    return "api"