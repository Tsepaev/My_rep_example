import pytest
import allure
from MainPage import MainPage


@pytest.fixture()
def driver() -> MainPage():
    main = MainPage()
    main.open_page("https://www.chitai-gorod.ru/")
    yield main
    main.close()


def test_search(driver):
    driver.search('Метро 2033')
    url = driver.get_url()
    catalog = driver.get_catalog()
    assert str(url).startswith("https://www.chitai-gorod.ru/search?phrase=") and catalog != []


def test_add_to_bucket(driver):
    driver.search("Game of Thrones")
    driver.select_book(2)
    driver.add_to_bucket()
    price, total_price = driver.check_price()
    assert price == total_price


@pytest.mark.parametrize("n", range(0,14))
def test_catalog(driver, n):
    driver.catalog_books(n)
