from time import sleep
import pytest
from MainPage import MainPage


def test_search():
    main = MainPage()
    main.open_page("https://www.chitai-gorod.ru/")
    main.search('Игра престоловsd 1452454514512')
    url = main.get_url()
    catalog = main.check_catalog()
    main.close()
    assert str(url).startswith("https://www.chitai-gorod.ru/search?phrase=") and catalog != []