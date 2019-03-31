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
dummy_user_email = "valid.dummy@email.com"

def create_dummy_user(cursor):
    global dummy_user_firstname, dummy_user_password, dummy_user_email
    #unassigned fields: id, created_at (autoassigned); modified_at, last_login_at (NULLed)
    developer_user_group = 3
    lastname = "Lastname"
    nickname = dummy_user_email
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
            (user_id, dummy_user_email, "email", "0", "12345678"))

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

def get_password_reset_token(cursor):
    user_id = get_dummy_userid(cursor)
    cursor.execute("SELECT token FROM user_password_reset_tokens WHERE user_id=%s", (user_id,))
    reset_token = cursor.fetchone()
    if reset_token is not None:
        reset_token = reset_token[0]
    return reset_token

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

def get_database_connection():
    import mysql.connector as mariadb

    db_connection = mariadb.connect(user='kbhffdk', password='localpass', database='kbhff_dk', port="54321")
    return db_connection

@pytest.fixture
def dummy_user():
    '''Create user with global dummy_user name and password'''
    db_connection = get_database_connection()
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

def try_login(driver, password):
    global dummy_user_email

    driver.get(pages["login"])

    login_url = driver.current_url

    username_entry = driver.find_element_by_id("input_username")
    username_entry.send_keys(dummy_user_email)

    password_entry = driver.find_element_by_id("input_password")
    password_entry.send_keys(password)
    password_entry.submit()
    
    import time
    time.sleep(0.5) #wait for driver to start loading next page
    # wait for page to load, up to ten seconds
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))

def driver_constructor_generator():
    driverlist = [webdriver.Firefox, webdriver.Chrome]
    yield from driverlist

def test_cantLoginWithBadCredentials():
    global dummy_user_email
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            try_login(driver, "thatsnotmypassword")
            assert "findes ikke" in driver.page_source

def test_canLoginWithGoodCredentials(dummy_user):
    global dummy_user_nickname
    global dummy_user_password
    for driver_constructor in driver_constructor_generator():
        with driver_constructor() as driver:
            try_login(driver, dummy_user_password)
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

    import time
    time.sleep(0.5) # wait for token to be written to database

    db_connection = get_database_connection()
    cursor = db_connection.cursor()
    reset_token = get_password_reset_token(cursor)

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

    try_login(driver, new_password)
    assert "<title>Login</title>" not in driver.page_source
    driver.quit()
