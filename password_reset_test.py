from selenium import webdriver
from navigation import *
from signup import *
from check_email import *



def test_canResetPassword():
    user_data = random_user_data()
    signup_via_webform(user_data)
    with webdriver.Firefox() as driver:
        request_password_reset(driver, user_data["email"])

        import time
        time.sleep(2) # wait for email
        mail = get_latest_mail_to(user_data["email"]) 
        token = get_password_reset_token_from_email(mail.body)

        fill_form_field(token, driver, form_id="input_reset-token")
        click_button(driver, class_name="button.primary")

        new_password = "averylongpasswordwithmorethan20characters"
        fill_form_field(new_password, driver, form_id="input_new_password")
        fill_form_field(new_password, driver, form_id="input_confirm_password")
        click_button(driver, class_name="button.primary")

        time.sleep(10)

if __name__ == "__main__":
    test_canResetPassword()
