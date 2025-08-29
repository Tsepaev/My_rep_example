from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest


URL = 'https://the-internet.herokuapp.com/'


@pytest.mark.parametrize("user, password, message",
    [
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
    ("Tom", "JustPassword", "Your username is invalid")
])
def test_log(user, password, message):
    driver = webdriver.Chrome()
    driver.get(URL + 'login')
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, "#username").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()
    url_local = driver.current_url
    if url_local == "https://the-internet.herokuapp.com/secure":
        logout = driver.find_element(By.CSS_SELECTOR, "a.button").text
        mes = driver.find_element(By.CSS_SELECTOR, "#flash").text
        assert logout == "Logout" and mes.startswith(message)
    else:
        mes = driver.find_element(By.CSS_SELECTOR, "#flash").text
        assert url_local == URL + "login" and mes.startswith(message)
    driver.quit()