from kbhff.api.navigation import *
from kbhff.api.webpage_patterns import get_verification_token_on_first_login
from kbhff.api.webpage_patterns import input_verification_token

def delete_user(user_data):
    """Deletes the given user by logging in and following the deletion flow.

    Positional arguments:
        user_data -- a dictionary containing the following keys:
                        email
                        password

    Raises InvalidUserError if user cannot log in.

    This method uses its own selenium driver, so doesn't disturb the flow of the enclosing test"""
    with webdriver.Firefox() as driver:
        try_login(driver, user_data["email"], user_data["password"])
        # if necessary, activate user before deletion
        if driver.current_url == pages["bekraeft_konto"]: 
            token = get_verification_token_on_first_login(user_data["email"])
            input_verification_token(token, driver)
            login(driver, user_data["email"], user_data["password"])
        click_button(driver, class_name="button.warning")
        click_button(driver, class_name="button.delete_me")
        fill_form_field(user_data["password"], driver, "input_password")
        click_button(driver, xpath="//form[@class='confirm_cancellation']/descendant::input[contains(@class, 'button')]") # "Farvel" button
        
        assert_current_page_is("login", driver, retryCount=10)
        assert_text_on_page("Dine oplysninger blev slettet", driver)
