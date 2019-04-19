import pytest
from kbhff.test.fixtures import *

from kbhff.api.navigation import *
from kbhff.api.webpage_patterns import *

import time


# Test specification number 1
def test_unverifiedUserFirstLogin(driver, unverified_user_via_medlemshjaelp):
    user = unverified_user_via_medlemshjaelp

    try_login(driver, user["email"], user["password"])
    verify_account_on_first_login(user["email"], driver)
    create_password(user["password"], driver)

    assert_current_page_is("kvittering", driver)

    navigate_to_page("login", driver)
    assert_username_prefilled(user["email"], driver)


# Test specification number 2
def test_unverifiedUserFirstLoginDuplicateVerificationTab(driver, unverified_user_via_medlemshjaelp):
    user = unverified_user_via_medlemshjaelp

    first_tab = navigate_to_page("login", driver)
    second_tab = navigate_to_page("login", driver, new_tab=True)

    driver.switch_to.window(first_tab)
    try_login(driver, user["email"], user["password"])
    assert_current_page_is("bekraeft_konto", driver)
    token = get_verification_token_on_first_login(user["email"])

    driver.switch_to.window(second_tab)
    navigate_to_page("bekraeft_konto", driver)
    input_verification_token(token, driver)
    create_password(user["password"], driver)
    assert_current_page_is("kvittering", driver)
    navigate_to_page("login", driver)
    assert_username_prefilled(user["email"], driver)

    driver.switch_to.window(first_tab)
    input_verification_token(token, driver)
    assert_current_page_is("login", driver)
    assert_username_prefilled(user["email"], driver)
    assert_text_on_page("Din konto er allerede aktiveret!", driver)


# Test specification number 3
def test_unverifiedUserFirstLoginDuplicatePasswordTab(driver, unverified_user_via_medlemshjaelp):
    user = unverified_user_via_medlemshjaelp

    first_tab = navigate_to_page("login", driver)
    second_tab = navigate_to_page("login", driver, new_tab=True)

    driver.switch_to.window(first_tab)
    try_login(driver, user["email"], user["password"])
    assert_current_page_is("bekraeft_konto", driver)
    token = get_verification_token_on_first_login(user["email"])
    input_verification_token(token, driver)
    assert_current_page_is("opret_password", driver)

    driver.switch_to.window(second_tab)
    navigate_to_page("opret_password", driver)
    create_password(user["password"], driver)
    assert_current_page_is("kvittering", driver)
    navigate_to_page("login", driver)
    assert_username_prefilled(user["email"], driver)

    driver.switch_to.window(first_tab)
    different_password = user["password"] + "different"
    create_password(different_password, driver)
    assert_current_page_is("login", driver)
    assert_username_prefilled(user["email"], driver)
    assert_text_on_page("Din konto har allerede en adgangskode!", driver)
