import pytest
import allure



def test_get_count_company(engine):
    print(engine.get_count_company())

@pytest.mark.parametrize('id, value', [(1666, False)])
def test_update_is_active(engine, id, value):
    engine.update_is_active(id=id, value=value)