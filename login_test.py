from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import subprocess
import pytest

pages = {}
pages["root"] = "http://kbhff.local/"
pages["login"] = pages["root"] + "login"

dummy_user_firstname = "3141592653" # very unlikely to clash with an existing user
dummy_user_password = "kbhff2357"
dummy_user_nickname = "valid.dummy@email.com"

def create_dummy_user(cursor):
    global dummy_user_firstname
    global dummy_user_password
    global dummy_user_nickname #"nickname" field seems to store the email address
    #unassigned fields: id, created_at (autoassigned); modified_at, last_login_at (NULLed)
    developer_user_group = 3
    lastname = "Lastname"
    nickname = dummy_user_nickname
    active_status = 1
    english = "EN"
    cursor.execute("INSERT IGNORE INTO users (user_group_id, firstname, lastname, " + \
        "nickname, status, language) VALUES (%s, %s, %s, %s, %s, %s)", \
        (developer_user_group, dummy_user_firstname, lastname, \
        nickname, active_status, english))

    user_id = get_dummy_userid(cursor)
    password_hash = get_php_password_hash(dummy_user_password)
    cursor.execute("INSERT IGNORE INTO user_passwords (user_id, password) VALUES (%s, %s)", \
            (user_id, password_hash))

    cursor.execute("INSERT IGNORE INTO user_usernames (user_id, username, type, " + \
            "verified, verification_code) VALUES (%s, %s, %s, %s, %s)", \
            (user_id, dummy_user_nickname, "email", "0", "12345678"))

def delete_dummy_user(cursor):
    user_id = get_dummy_userid(cursor)
    if user_id is not None:
        cursor.execute("DELETE FROM user_passwords WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM user_usernames WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))


def get_php_password_hash(plaintext_password):
    '''Generate hash of plaintext password in php, return the hash.
    Make sure "password_hash.php" contains the hashing algorithm used in the application.'''
    result = subprocess.run(
            ["php", "password_hash.php", plaintext_password],
            stdout = subprocess.PIPE,
            check = True
            )
    return result.stdout.decode("UTF-8")

def get_dummy_userid(cursor):
    global dummy_user_firstname
    cursor.execute("SELECT id FROM users WHERE firstname=%s", (dummy_user_firstname,))
    user_id = cursor.fetchone()
    if user_id is not None:
        user_id = user_id[0]
    return user_id

def get_password_hash_by_userid(user_id, cursor):
    cursor.execute("SELECT password FROM user_passwords WHERE user_id=%s", (user_id,))
    password_hash =  cursor.fetchone()
    if password_hash is not None:
        password_hash = password_hash[0]
    return password_hash


@pytest.fixture
def dummy_user():
    '''Create user with globl dummy_user name and password'''
    import mysql.connector as mariadb

    db_connection = mariadb.connect(user='kbhffdk', password='localpass', database='kbhff_dk')
    cursor = db_connection.cursor()

    delete_dummy_user(cursor)
    create_dummy_user(cursor)
    user_id = get_dummy_userid(cursor)
    assert user_id is not None
    password_hash = get_password_hash_by_userid(user_id, cursor)
    assert password_hash is not None

    db_connection.commit()

    yield None # separates setup from teardown

    delete_dummy_user(cursor)
    db_connection.commit()


def driver_constructor_generator():
    driverlist = [webdriver.Firefox, webdriver.Chrome]
    yield from driverlist


def test_cantLoginWithBadCredentials():
    global dummy_user_nickname
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            driver.get(pages["login"])

            username_entry = driver.find_element_by_id("input_username")
            username_entry.send_keys("dont@email.me")

            password_entry = driver.find_element_by_id("input_password")
            password_entry.send_keys("thatsnotmypassword")
            password_entry.submit()

            #wait until the error message appears, or 10 seconds, whichever is shorter
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class='error']")))

            assert "forkert brugernavn eller password" in driver.page_source


def test_canLoginWithGoodCredentials(dummy_user):
    global dummy_user_nickname
    global dummy_user_password
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            driver.get(pages["login"])

            username_entry = driver.find_element_by_id("input_username")
            username_entry.send_keys(dummy_user_nickname)

            password_entry = driver.find_element_by_id("input_password")
            password_entry.send_keys(dummy_user_password)
            import time
            time.sleep(3)
            password_entry.submit()

            import time
            time.sleep(3)
            #wait until redirected to new page, or 10 seconds, whichever is shorter
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))

            assert "<title>Login</title>" not in driver.page_source

