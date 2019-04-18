from navigation import *

def delete_user(user_data):
    """Deletes the given user by logging in and following the deletion flow.

    Positional arguments:
        user_data -- a dictionary containing the following keys:
                        email
                        password

    Raises InvalidUserError if user cannot log in.

    This method uses its own selenium driver, so doesn't disturb the flow of the enclosing test"""
    with webdriver.Firefox() as driver:
        login(driver, user_data["email"], user_data["password"])
        click_button(driver, class_name="button.warning")
        click_button(driver, class_name="button.delete_me")
        fill_form_field(user_data["password"], driver, "input_password")
        click_button(driver, xpath="//form[@class='confirm_cancellation']/descendant::input[contains(@class, 'button')]") # "Farvel" button
        
        wait_for_next_page(driver)
        assert_current_page_is("login", driver, retryCount=10)
        assert_text_on_page("Dine oplysninger blev slettet", driver)