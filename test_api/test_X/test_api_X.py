import requests
import allure
import pytest
from MainAPI import MainAPI

"leyla, water-fairy"


@pytest.fixture()
def api():
    resp = MainAPI()
    return resp


def test_auth(api):
    status, token = api.get_token()
    assert status == 201


@pytest.mark.parametrize("active, isActive", [(None, True), (True, True), (False, False)])
def test_get_company(api, active, isActive: bool):
    status, company_list = api.get_company(active)
    assert status == 200 and company_list[0]["isActive"] == isActive


def test_create_company(api):
    status, resp_id = api.create_company("SimpleCompany", "SimpleDesc")
    assert status == 201


@pytest.mark.parametrize("id_company, stat", [(1629, 200)])
def test_get_company_by_id(api, id_company, stat):
    status, resp_id = api.get_company_by_id(id_company)
    assert status == stat and resp_id == id_company


@pytest.mark.xfail(reason="Ожидаем статус 404, возвращает 200 без Body")
@pytest.mark.parametrize("id_company, stat", [(200000, 404)])
def test_get_company_by_id_error(api, id_company, stat):
    status, resp_id = api.get_company_by_id(id_company)
    assert status == stat and resp_id == id_company


def test_delete_company(api):
    api.create_company("SimpleCompany", "SimpleDesc")