import pytest
import allure



def test_get_count_company(engine):
    print(engine.get_count_company())

def test_get_company_by_id(engine):
    print(engine.get_company_by_id(1629))

@pytest.mark.parametrize('id, value', [(1666, False)])
def test_update_is_active(engine, id, value):
    engine.update_is_active(id=id, value=value)


@pytest.mark.parametrize("id", [1, 2])
def test_delete_company_by_id(engine, id):
    with allure.step("Удалить компанию с указанным id"):
        engine.delete_company_by_id(id)
    with allure.step("Проверить, что компания отсутствует в БД"):
        lst = engine.get_company_by_id(id)
        assert lst == []

@pytest.mark.skip("Для наполнения таблицы компаниями")
def test_create_company(engine):
    for i in range(1, 30):
        engine.create_company(i, True, f"VeryCoolCompany_{i}")