from time import sleep
import pytest
from MainPage import MainPage


def test_search():
    main = MainPage()
    main.open_page("https://www.chitai-gorod.ru/")
    main.search('Метро 2033')
    url = main.get_url()
    catalog = main.get_catalog()
    main.close()
    assert str(url).startswith("https://www.chitai-gorod.ru/search?phrase=") and catalog != []


def test_add_to_bucket():
    main = MainPage()
    main.open_page("https://www.chitai-gorod.ru/")
    main.search("Game of Thrones")
    main.select_book(2)
    main.add_to_bucket()
    price, total_price = main.check_price()
    main.close()
    assert price == total_price


def test_catalog_books():
    main = MainPage()
    main.open_page("https://www.chitai-gorod.ru/")
    main.catalog_books()

    main.close()
