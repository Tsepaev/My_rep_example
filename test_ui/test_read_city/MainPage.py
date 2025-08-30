from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class MainPage:


    def __init__(self, driver = WebDriver):
        self.driver = driver


    def open_page(self, url):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(6)


    def search(self, book: str):
        sleep(2)
        waiter = WebDriverWait(self.driver, 5)
        self.driver.find_element(By.CSS_SELECTOR, ".search-form__input").send_keys(book)
        waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".suggests-list")))
        self.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        sleep(2)


    def get_url(self):
        return self.driver.current_url

    def check_catalog(self) -> list:
        return self.driver.find_elements(By.CSS_SELECTOR, ".product-card")


    def close(self):
        self.driver.quit()
