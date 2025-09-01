from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import allure

class MainPage:


    def __init__(self, driver = WebDriver):
        self.driver = driver
        self.buy_button = (By.CSS_SELECTOR, ".product-buttons .chg-app-button--primary")

    def open_page(self, url):
        """Открыть страницу. Вписать url'"""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(6)
        auth = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".popmechanic-main")))
        if auth.is_displayed():
            js = "document.querySelector('.popmechanic-main').remove()"
            self.driver.execute_script(js)
        self.driver.find_element(By.CSS_SELECTOR, '.agreement-notice button').click()


    def search(self, book: str):
        """Поиск. Вписать название книги"""
        waiter = WebDriverWait(self.driver, 5)
        self.driver.find_element(By.CSS_SELECTOR, ".search-form__input").send_keys(book)
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".suggests-list")))
        self.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        sleep(2)


    def get_url(self):
        return self.driver.current_url


    def get_catalog(self) -> list:
        return self.driver.find_elements(By.CSS_SELECTOR, ".product-card")


    def select_book(self, n: int):
        """Выбрать книгу с индексом. Вписать индекс списка"""
        catalog = self.driver.find_elements(By.CSS_SELECTOR, ".product-card")
        catalog[n].click()


    def add_to_bucket(self):
        WebDriverWait(self.driver, 5).\
            until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-buttons .chg-app-button--primary")))
        with allure.step("Кликнуть по кнопке 'купить'"):
            self.driver.find_element(By.CSS_SELECTOR, ".product-buttons .chg-app-button--primary").click()
        WebDriverWait(self.driver, 5).\
            until(EC.text_to_be_present_in_element(self.buy_button, "Оформить"))
        with allure.step("Кликнуть по кнопке 'оформить'"):
            self.driver.find_element(By.CSS_SELECTOR, ".product-buttons .chg-app-button--primary").click()
        WebDriverWait(self.driver, 5).\
            until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-sidebar__footer")))


    def check_price(self):
        """Возвращает цену книги (price) и сумму к заказу (total_price)"""
        price = self.driver.find_element(By.CSS_SELECTOR, ".product-price__price").text
        total_price = self.driver.find_element(By.CSS_SELECTOR, ".cart-sidebar__item-summary .info-item__value").text
        return price, total_price


    def close(self):
        self.driver.quit()


    def category_books(self, n: int = 0) -> list:
        """Клик по каталогу, далее книги, получить список категорий и кликнуть по указанной"""
        with allure.step("Кликнуть по кнопке 'Каталог'"):
            self.driver.find_element(By.CSS_SELECTOR, ".catalog-btn").click()
        with allure.step("Кликнуть по разделу 'Книги'"):
            self.driver.find_element(By.CSS_SELECTOR, ".categories-level-menu .categories-level-menu__item--active").click()
        list_booktype = self.driver.find_elements(By.CSS_SELECTOR, ".categories-level-menu")[1].\
            find_elements(By.CSS_SELECTOR, ".categories-level-menu__item")
        with allure.step(f"Кликнуть по {n+1} категории"):
            list_booktype[n].click()
        return list_booktype


    def list_books(self) -> list:
        list_books = self.driver.find_elements(By.CSS_SELECTOR, ".categories-level-menu")[2]. \
            find_elements(By.CSS_SELECTOR, "a")
        return list_books


    def catalog_books(self, n):
        """Задать индекс подкатегории n"""
        self.category_books(n)
        list_books = self.list_books()
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".categories-menu__close").click()
        sleep(1)
        for i in range(0, len(list_books)):
            self.category_books(n)
            list_books = self.list_books()
            link = list_books[i].get_dom_attribute("href")
            with allure.step(f"Кликнуть по {i+1} подкатегории"):
                list_books[i].click()
            sleep(1)
            url_link = self.driver.current_url
            with allure.step("Проверить что url страницы соответствует выбранной подкатегории"):
                assert str(url_link) == "https://www.chitai-gorod.ru" + str(link)