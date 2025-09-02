import allure
import pytest
from MainAPI import MainAPI


@pytest.fixture()
def api():
    resp = MainAPI()
    return resp


def test_auth(api):
    status, token = api.get_token()
    assert status == 201


@allure.suite("Функционал API")
@allure.title("Проверка. Запрос списка компании")
@allure.tag("API", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("http://51.250.26.13:8083/", name="X-client")
@pytest.mark.parametrize("active, isActive", [(None, True), (True, True), (False, False)])
def test_get_company(api, active, isActive: bool):
    status, company_list = api.get_company(active)
    assert status == 200 and company_list[0]["isActive"] == isActive


@allure.suite("Функционал API")
@allure.title("Проверка. Добавить компанию")
@allure.tag("API", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("http://51.250.26.13:8083/", name="X-client")
def test_create_company(api):
    status, resp_id = api.create_company("SimpleCompany", "SimpleDesc")
    assert status == 201


@allure.suite("Функционал API")
@allure.title("Проверка. Получить компанию по id")
@allure.tag("API", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("http://51.250.26.13:8083/", name="X-client")
@pytest.mark.parametrize("id_company, stat", [(1629, 200)])
def test_get_company_by_id(api, id_company, stat):
    status, resp_id = api.get_company_by_id(id_company)
    assert status == stat and resp_id == id_company


@allure.suite("Функционал API")
@allure.title("Проверка. Получить компанию по не корректному id")
@allure.tag("API", "Functional")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("http://51.250.26.13:8083/", name="X-client")
@pytest.mark.xfail(reason="Ожидаем статус 404, возвращает 200 без Body")
@pytest.mark.parametrize("id_company, stat", [(200000, 404)])
def test_get_company_by_id_error(api, id_company, stat):
    status, resp_id = api.get_company_by_id(id_company)
    assert status == stat and resp_id == id_company


@allure.suite("Функционал API")
@allure.title("Проверка. Удалить компанию")
@allure.tag("API", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("http://51.250.26.13:8083/", name="X-client")
def test_delete_company(api):
    with allure.step("Получить список компаний. Узнать длину списка"):
        stat, company_list_before = api.get_company(None)
    with allure.step("Добавить новую компанию"):
        status_token, token = api.get_token()
        status, resp_id = api.create_company("SimpleTESTCompany", "SimpleTESTDesc", token)
    with allure.step("Удалить добавленную компанию"):
        status_delete = api.delete_company(resp_id, token)
    with allure.step("Получить список компаний. Узнать длину списка"):
        stat, company_list_after = api.get_company(None)
    with allure.step(
            "Проверить статус команды удаления компании. Проверить, что длина списка в начале теста и в конце теста не изменилась"):
        assert status_delete == 200 and len(company_list_before) == len(company_list_after)


@allure.suite("Функционал API")
@allure.title("Проверка. Изменить статус компании")
@allure.tag("API", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("http://51.250.26.13:8083/", name="X-client")
def test_change_status(api):
    with allure.step("Добавить новую компанию"):
        status_token, token = api.get_token()
        status, resp_id = api.create_company("SimpleTESTCompanyOne", "SimpleTESTDescTwo", token)
    with allure.step("Изменить статус созданной компании на False"):
        status_company, status_active = api.change_status(resp_id, token, False)
    with allure.step("Проверить статус кода и статус активации компании"):
        assert status_company == 200 and status_active == False
