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

def request_password_reset(driver, user_email):
    driver.get(pages["login"])

    forgot_password_link = driver.find_element_by_xpath("//p[@class='forgot']/a")
    forgot_password_link.click()

    WebDriverWait(driver, 10).until(EC.url_changes(pages["login"]))

    email_entry = driver.find_element_by_id("input_username")
    email_entry.send_keys(user_email)
    email_entry.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_reset-token")))

    # wait for token to be written to database
    time.sleep(0.5) 

def enter_password_request_token(driver, reset_token):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_reset-token")))

    reset_token_entry = driver.find_element_by_id("input_reset-token")
    reset_token_entry.send_keys(reset_token)
    reset_token_entry.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_new_password")))

def enter_new_password_for_reset(driver, new_password):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_new_password")))
    password_entry = driver.find_element_by_id("input_new_password")
    password_entry.send_keys(new_password)

    password_confirm = driver.find_element_by_id("input_confirm_password")
    password_confirm.send_keys(new_password)
    password_confirm.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_username")))

