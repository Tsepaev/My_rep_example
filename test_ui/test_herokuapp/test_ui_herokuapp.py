from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import pytest


URL = 'https://the-internet.herokuapp.com/'


@pytest.mark.parametrize("user, password, message",
    [
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
    ("Tom", "JustPassword", "Your username is invalid")
])
def test_auth(user, password, message):
    """Проверка авторизации пользователя"""
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


def test_context_menu():
    """Проверка вызова контекстного меню + alert"""
    driver = webdriver.Chrome()
    driver.get(URL + 'context_menu')
    driver.maximize_window()
    driver.implicitly_wait(5)
    actions = ActionChains(driver)
    actions.context_click(driver.find_element(By.CSS_SELECTOR, "#hot-spot")).perform()
    mes = driver.switch_to.alert.text
    driver.switch_to.alert.accept()
    check = driver.find_element(By.CSS_SELECTOR, "a[target]").is_enabled()
    assert mes == "You selected a context menu" and check
    driver.quit()


def test_drag_and_drop():
    """Проверка успешного перемещения элемента"""
    driver = webdriver.Chrome()
    driver.get(URL + 'drag_and_drop')
    driver.maximize_window()
    driver.implicitly_wait(5)
    actions = ActionChains(driver)
    a = driver.find_element(By.CSS_SELECTOR, "#column-a")
    b = driver.find_element(By.CSS_SELECTOR, "#column-b")
    actions.drag_and_drop(a, b).perform()
    assert a.text == "B"
    driver.quit()


def test_scroll():
    """Cкроллинг страницы"""
    driver = webdriver.Chrome()
    driver.get(URL + 'infinite_scroll')
    driver.maximize_window()
    driver.implicitly_wait(5)
    actions = ActionChains(driver)
    for i in range(1,10):
        actions.scroll_by_amount(0, 800).pause(1).perform()
    driver.quit()
