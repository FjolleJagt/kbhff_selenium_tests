from navigation import *


def signup_skipping_verification_step(user_data):
    """Create a user by going through the signup flow, but skipping the verification step.

    Positional arguments:
        user_data -- a dictionary containing the following keys:
                        email
                        password
                        (others? address etc.)

    This method uses its own selenium driver, so doesn't disturb the flow of the enclosing test"""
    with webdriver.Firefox() as driver:
        navigate_to_page("signup", driver)


if __name__ == "__main__":
    with webdriver.Firefox() as driver:
        user_data = {}
        user_data["email"] = "not@an.actual.mail.dlghh.dk"
        user_data["firstname"] = "a new firstname"
        user_data["lastname"] = "and a new lastname"
        user_data["password"] = "password"
        user_data["department"] = "Vesterbro"
        time.sleep(1)
        navigate_to_page("signup", driver)
        time.sleep(1)
        click_button(driver, class_name = "button.primary")
        time.sleep(1)
        fill_form_field(user_data["firstname"], driver, form_id="input_firstname")
        time.sleep(1)
        fill_form_field(user_data["lastname"], driver, form_id="input_lastname")
        time.sleep(1)
        fill_form_field(user_data["email"], driver, form_id="input_email")
        fill_form_field(user_data["email"], driver, form_id="input_confirm_email")
        time.sleep(1)
        fill_form_field(user_data["password"], driver, form_id="input_password")
        time.sleep(1)
        select_from_dropdown(user_data["department"], driver, "input_department_id")
        time.sleep(1)
        check_checkbox(driver, "input_terms")
        time.sleep(1)
        submit_form(driver)



        time.sleep(10)
