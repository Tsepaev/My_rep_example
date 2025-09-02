import pytest
from test_api.test_X.MainAPI import MainAPI
from test_SQL.MainSQL import MainSQL


@pytest.fixture()
def api():
    resp = MainAPI()
    return resp

@pytest.fixture()
def engine():
    engine = MainSQL()
    return engine
