from navigation import *
from check_email import *

verify_account_on_first_login(user_email, driver):
    assert_currect_page_is("bekraeft_konto", driver)
    mail = get_latest_mail_to(user_email, expect_title="Aktiver din konto hos KBHFF", retryCount=5)
    token = get_activation_code_from_email(mail.body)
    fill_form_field(token, driver, form_id="input_verification_code")
    submit_form(driver)

create_password(new_password, driver):
    assert_current_page_is("opret_password", driver)
    fill_form_field(new_password, driver, form_id="input_new_password")
    fill_form_field(new_password, driver, form_id="input_confirm_password")
    submit_form(driver)

