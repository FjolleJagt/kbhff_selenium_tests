import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

pages = {}
pages["root"] = "http://kbhff.local/"
pages["login"] = pages["root"] + "login"

def try_login(driver, username, password):

    driver.get(pages["login"])

    login_url = driver.current_url

    username_entry = driver.find_element_by_id("input_username")
    username_entry.send_keys(username)

    password_entry = driver.find_element_by_id("input_password")
    password_entry.send_keys(password)
    password_entry.submit()
    
    # wait for driver to start loading next page
    time.sleep(0.5)
    # wait for page to load, up to ten seconds
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))
