import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions





@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys('g@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('1234')
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

    yield driver

    driver.quit()