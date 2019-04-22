from kbhff.api.navigation import *
from kbhff.api.email import *

def get_verification_token_on_first_login(user_email, email_connection=None):
    mail = get_latest_mail_to(user_email, email_connection=email_connection, expect_title="Aktiver din konto hos KBHFF", retryCount=25)
    return get_activation_code_from_email(mail.body)

def input_verification_token(token, driver):
    assert_current_page_is("bekraeft_konto", driver)
    fill_form_field(token, driver, form_id="input_verification_code")
    submit_form(driver)

def verify_account_on_first_login(user_email, driver, email_connection=None):
    token = get_verification_token_on_first_login(user_email, email_connection)
    input_verification_token(token, driver)

def create_password(new_password, driver):
    assert_current_page_is("opret_password", driver)
    fill_form_field(new_password, driver, form_id="input_new_password")
    fill_form_field(new_password, driver, form_id="input_confirm_password")
    submit_form(driver)

def assert_username_prefilled(username, driver):
    assert_current_page_is("login", driver)
    assert get_form_field_value(driver, form_id="input_username") == username

def assert_username_not_prefilled(driver):
    assert_current_page_is("login", driver)
    assert get_form_field_value(driver, form_id="input_username") == "Brugernavn"
