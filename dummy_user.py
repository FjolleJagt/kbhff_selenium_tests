from database_interaction import *
import pytest

dummy_user_firstname = "3141592653" # very unlikely to clash with an existing user
dummy_user_password = "kbhff2357"
dummy_user_email = "cb.open.automail+dummyUserKBHFF@gmail.com"

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

def get_dummy_userid(cursor):
    global dummy_user_firstname
    cursor.execute("SELECT id FROM users WHERE firstname=%s", (dummy_user_firstname,))
    user_id = cursor.fetchone()
    if user_id is not None:
        user_id = user_id[0]
    return user_id

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

