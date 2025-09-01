import pytest
import allure
from MainPage import MainPage


@pytest.fixture()
def driver() -> MainPage():
    main = MainPage()
    with allure.step("Открыть клиент. Перейти на страницу https://www.chitai-gorod.ru/"):
        main.open_page("https://www.chitai-gorod.ru/")
    yield main
    main.close()


@allure.suite("Функционал сайта")
@allure.title("Проверка поиска книги по названию")
@allure.tag("UI", "Functional")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("https://www.chitai-gorod.ru/", name="Читай-город")
def test_search(driver):
    with allure.step("В поле поиска ввести название книги и нажать на 'Поиск'"):
        driver.search('Метро 2033')
    url = driver.get_url()
    catalog = driver.get_catalog()
    with allure.step("Проверить что в url добавлены параметры 'поиск по фразе' и название книги. Проверить, что список книг не пустой"):
        assert str(url).startswith("https://www.chitai-gorod.ru/search?phrase=") and catalog != []


@allure.suite("Функционал сайта")
@allure.title("Проверка добавления товара в корзину")
@allure.tag("UI", "Functional")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("https://www.chitai-gorod.ru/", name="Читай-город")
def test_add_to_bucket(driver):
    with allure.step("В поле поиска ввести название книги и нажать на 'Поиск'"):
        driver.search("Game of Thrones")
    with allure.step("Выбрать книгу и кликнуть по картинке"):
        driver.select_book(0)
    driver.add_to_bucket()
    price, total_price = driver.check_price()
    with allure.step("Проверить, что цена товара соответствует цене 'Итого'"):
        assert price == total_price


@allure.suite("Функционал сайта")
@allure.sub_suite("Каталог. Книги")
@allure.title("Проверка работоспособности раздела 'Книги'")
@allure.tag("UI", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("https://www.chitai-gorod.ru/", name="Читай-город")
@pytest.mark.parametrize("n", range(0,3)) # Второе число должно быть 14. Уменьшил для ускорения прогона.
def test_catalog(driver, n):
    driver.catalog_books(n)


@allure.suite("Функционал сайта")
@allure.title("Проверка корректности установленной скидки")
@allure.tag("UI", "Functional")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Tsepaev Denis")
@allure.link("https://www.chitai-gorod.ru/", name="Читай-город")
@pytest.mark.parametrize('n', [0 , 2, 4])
def test_sales(driver, n:int):
    with allure.step("Кликнуть по кнопке 'Распродажа'"):
        driver.get_sales()
    with allure.step(f"Проверить, что итоговая цена {n+1} книги, указана корректно"):
        price_after_disc, new_price = driver.check_sale(n)
        assert int(price_after_disc) == int(new_price)

