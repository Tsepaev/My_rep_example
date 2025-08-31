from time import sleep
import pytest
from MainPage import MainPage


@pytest.fixture()
def setting() -> MainPage():
    main = MainPage()
    main.open_page("https://www.chitai-gorod.ru/")
    yield main
    main.close()


def test_search(setting):
    setting.search('Метро 2033')
    url = setting.get_url()
    catalog = setting.get_catalog()

    assert str(url).startswith("https://www.chitai-gorod.ru/search?phrase=") and catalog != []


def test_add_to_bucket(setting):
    setting.search("Game of Thrones")
    setting.select_book(2)
    setting.add_to_bucket()
    price, total_price = setting.check_price()
    assert price == total_price


def test_catalog_books_fiction(setting):
    setting.catalog_books(0)


def test_catalog_books_young_adult(setting):
    setting.catalog_books(1)


def test_catalog_books_educational_literature(setting):
    setting.catalog_books(2)


def test_catalog_books_psychology(setting):
    setting.catalog_books(3)
