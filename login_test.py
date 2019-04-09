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
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            navigate_to_page("login", driver)

            forgot_password_link = driver.find_element_by_xpath("//p[@class='forgot']/a") 
            forgot_password_link.click()

            email_entry = driver.find_element_by_id("input_username")
            email_entry.send_keys(user_email)
            email_entry.submit()

            time.sleep(3) # wait for email to be sent
            mail = get_latest_mail_to(dummy_user_email)
            reset_token = get_password_reset_code_from_email(mail.body)

            fill_form_field(reset_token, driver, form_id="input_reset-token")
            submit_form(driver)

            new_password = dummy_user_password + "notSame"
            enter_new_password_for_reset(driver, new_password)

            fill_form_field(new_password, driver, form_id="input_new_password")
            fill_form_field(new_password, driver, form_id="input_confirm_password")
            submit_form(driver)

            try_login(driver, dummy_user_email, new_password)
            assert "<title>Login</title>" not in driver.page_source
