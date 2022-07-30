from fastapi.testclient import TestClient

from . import __main__

client = TestClient(__main__.app)
