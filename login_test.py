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
            request_password_reset(driver, dummy_user_email)

            db_connection = get_database_connection()
            cursor = db_connection.cursor()
            user_id = get_dummy_userid(cursor)
            reset_token = get_password_reset_token_by_userid(user_id, cursor)

            enter_password_request_token(driver, reset_token)

            new_password = dummy_user_password + "notSame"
            enter_new_password_for_reset(driver, new_password)

            try_login(driver, dummy_user_email, new_password)
            assert "<title>Login</title>" not in driver.page_source
