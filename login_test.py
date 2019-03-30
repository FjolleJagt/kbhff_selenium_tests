from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pytest

from navigation import *
from database_interaction import *
from dummy_user import *


def driver_constructor_generator():
    driverlist = [webdriver.Firefox, webdriver.Chrome]
    yield from driverlist

def test_cantLoginWithBadCredentials():
    global dummy_user_email
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            try_login(driver, dummy_user_email, "thatsnotmypassword")
            assert "findes ikke" in driver.page_source

def test_canLoginWithGoodCredentials(dummy_user):
    global dummy_user_nickname
    global dummy_user_password
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            try_login(driver, dummy_user_email, dummy_user_password)
            assert "<title>Login</title>" not in driver.page_source


def test_canResetPassword(dummy_user):
    global dummy_user_email, dummy_user_password
    driver = webdriver.Firefox()
    driver.get(pages["login"])

    forgot_password_link = driver.find_element_by_xpath("//p[@class='forgot']/a")
    forgot_password_link.click()

    WebDriverWait(driver, 10).until(EC.url_changes(pages["login"]))

    email_entry = driver.find_element_by_id("input_username")
    email_entry.send_keys(dummy_user_email)
    email_entry.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_reset-token")))

    # wait for token to be written to database
    time.sleep(0.5) 

    db_connection = get_database_connection()
    cursor = db_connection.cursor()
    user_id = get_dummy_userid(cursor)
    reset_token = get_password_reset_token_by_userid(user_id, cursor)

    reset_token_entry = driver.find_element_by_id("input_reset-token")
    reset_token_entry.send_keys(reset_token)
    reset_token_entry.submit()

    new_password = dummy_user_password + "butDifferent"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_new_password")))
    password_entry = driver.find_element_by_id("input_new_password")
    password_entry.send_keys(new_password)

    password_confirm = driver.find_element_by_id("input_confirm_password")
    password_confirm.send_keys(new_password)
    password_confirm.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_username")))

    try_login(driver, dummy_user_email, new_password)
    assert "<title>Login</title>" not in driver.page_source
    driver.quit()
