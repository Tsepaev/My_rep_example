from sqlalchemy import create_engine, text
import pytest
import allure

from MainSQL import MainSQL


@pytest.fixture()
def engine():
    engine = MainSQL()


