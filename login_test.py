import pytest
from fixtures import *

from navigation import *
from check_email import *

import time


# Test specification number 1
def test_unverifiedUserFirstLogin(driver, unverified_user_via_medlemshjaelp):
    user = unverified_user_via_medlemshjaelp

    try_login(driver, user["email"], user["password"])
    assert_current_page_is("bekraeft_konto", driver)

    time.sleep(2) # wait for email to be sent
    mail = get_latest_mail_to(user["email"], expect_title="Aktiver din konto hos KBHFF", retry=5)
    token = get_activation_code_from_email(mail.body)
    fill_form_field(token, driver, form_id="input_verification_code")
    submit_form(driver)
    assert_current_page_is("opret_password", driver)

    fill_form_field(user["password"], driver, form_id="input_new_password")
    fill_form_field(user["password"], driver, form_id="input_confirm_password")
    submit_form(driver)
    assert_current_page_is("kvittering", driver)

    navigate_to_page("login", driver)
    assert_current_page_is("login", driver)
    assert get_form_field_value(driver, form_id="input_username") == user["email"]



