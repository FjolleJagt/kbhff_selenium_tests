from navigation import *

dummy_card = {}
dummy_card["number"] = "4242 4242 4242 4242"
dummy_card["MM"] = "12"
dummy_card["YY"] = "20"
dummy_card["CVC"] = "123"

def random_string(n):
    import string, random
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def random_user_data():
    import random
    user_data = {}
    user_data["email"] = random_string(10) + "@kbhff.dk"
    user_data["firstname"] = random_string(10)
    user_data["lastname"] = random_string(10)
    user_data["password"] = random_string(15)
    user_data["department"] = random.choice(["Vesterbro", "Amager"])

    return user_data 


def signup_skipping_verification_step(user_data):
    """Create a user by going through the signup flow, but skipping the verification step.

    Positional arguments:
        user_data -- a dictionary containing the following keys:
                        firstname
                        lastname
                        email
                        password
                        department ("Vesterbro" or "Amager")

    This method uses its own selenium driver, so doesn't disturb the flow of the enclosing test"""
    with webdriver.Firefox() as driver:
        navigate_to_page("signup", driver)
        click_button(driver, class_name = "button.primary")
        fill_form_field(user_data["firstname"], driver, form_id="input_firstname")
        fill_form_field(user_data["lastname"], driver, form_id="input_lastname")
        fill_form_field(user_data["email"], driver, form_id="input_email")
        fill_form_field(user_data["email"], driver, form_id="input_confirm_email")
        fill_form_field(user_data["password"], driver, form_id="input_password")
        select_from_dropdown(user_data["department"], driver, "input_department_id")
        check_checkbox(driver, "input_terms")
        submit_form(driver)

        click_button(driver, class_name = "skip") #skips verification step
        
        global dummy_card
        fill_form_field(dummy_card["number"], driver, form_id="input_card_number")
        fill_form_field(dummy_card["MM"], driver, form_id="input_card_exp_month")
        fill_form_field(dummy_card["YY"], driver, form_id="input_card_exp_year")
        fill_form_field(dummy_card["CVC"], driver, form_id="input_card_cvc")
        submit_form(driver)
        
        time.sleep(5) # payment takes particularly long... need a better way to wait.
        wait_for_next_page(driver)
        assert("er godkendt" in driver.page_source) # signup and payment were successful

if __name__ == "__main__":
    user_data = random_user_data()
    signup_skipping_verification_step(user_data)
    with webdriver.Firefox() as driver:
        try_login(driver, user_data["email"], user_data["password"])
        time.sleep(3)



