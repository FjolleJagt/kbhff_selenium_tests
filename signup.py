from navigation import *
from check_email import *

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
    user_data["email"] = "cb.open.automail+" + random_string(10) + "@gmail.com"
    user_data["firstname"] = random_string(10)
    user_data["lastname"] = random_string(10)
    user_data["password"] = random_string(15)
    user_data["department"] = random.choice(["Vesterbro", "Amager"])
    user_data["membershiptype"] = random.choice(["Frivillig", "Støttemedlem"])

    return user_data 

def _signup_step_data_entry(driver, user_data):
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

def _signup_step_betaling(driver):
        global dummy_card
        fill_form_field(dummy_card["number"], driver, form_id="input_card_number")
        fill_form_field(dummy_card["MM"], driver, form_id="input_card_exp_month")
        fill_form_field(dummy_card["YY"], driver, form_id="input_card_exp_year")
        fill_form_field(dummy_card["CVC"], driver, form_id="input_card_cvc")
        submit_form(driver)
        
        wait_for_next_page(driver)
        assert_text_on_page("er godkendt", driver, retry=10)

def _signup_step_verification(email, driver):
        mail = get_latest_mail_to(email)
        activation_code = get_activation_code_from_email(mail.body)
        fill_form_field(activation_code, driver, form_id="input_verification_code")
        submit_form(driver)

def signup_via_webform(user_data, activate_right_away=True):
    """Create a user by going through the signup flow.

    Positional arguments:
        user_data -- a dictionary containing the following keys:
                        firstname
                        lastname
                        email
                        password
                        department ("Vesterbro" or "Amager")

    This method uses its own selenium driver, so doesn't disturb the flow of the enclosing test"""
    with webdriver.Firefox() as driver:
        _signup_step_data_entry(driver, user_data)

        if activate_right_away:
            time.sleep(10)# wait for email
            _signup_step_verification(user_data["email"], driver)
        else:
            click_button(driver, class_name = "skip") #skips verification step

        _signup_step_betaling(driver)

def signup_via_medlemshjaelp(vagt_user_data, signup_data, payment="mobilepay"):
    """Log in as a Butiksvagt and creates a user with the requested email address using the medlemshjælp page.

    Positional arguments:
        signup_data -- a dictionary containing the following keys: 
            "firstname", 
            "lastname",
            "email",
            "membershiptype" (in ["Frivillig", "Støttemedlem"])
            "department" (in ["Vesterbro", "Amager"])
        vagt_user_data -- a dictionary containing the following keys:
            "email",
            "password" -- used to log in as existing member on butiksvagt
        payment (in ["mobilepay", "cash", "skip"])

    This method uses its own selenium driver, so doesn't disturb the flow of the enclosing test"""
    with webdriver.Firefox() as driver:
        try_login(driver, vagt_user_data["email"], vagt_user_data["password"])
        assert_current_page_is("min_side", driver)
        navigate_to_page("medlemshjaelp-signup", driver)
        assert_current_page_is("medlemshjaelp-signup", driver)
        
        fill_form_field(signup_data["firstname"], driver, form_id="input_firstname")
        fill_form_field(signup_data["lastname"], driver, form_id="input_lastname")
        fill_form_field(signup_data["email"], driver, form_id="input_email")
        fill_form_field(signup_data["email"], driver, form_id="input_confirm_email")
        select_from_dropdown(signup_data["membershiptype"], driver, "input_item_id")
        select_from_dropdown(signup_data["department"], driver, "input_department_id")
        check_checkbox(driver, "input_terms")
        submit_form(driver)

        wait_for_next_page(driver)
        
        if payment == "mobilepay":
            check_checkbox(driver, "input_confirm_mobilepay_payment")
            
            # mobilepay payment submit button
            click_button(driver, xpath="/html/body/div/div[3]/div/div/form[1]/ul/li/input")

        elif payment == "cash":
            # Display cash payment options
            click_button(driver, xpath="/html/body/div/div[3]/div/div/h4[2]")

            check_checkbox(driver, "input_confirm_cash_payment")

            # cash payment submit button
            click_button(driver, xpath="/html/body/div/div[3]/div/div/form[2]/ul/li[2]/input")

        elif payment == "skip":
            # Display cash payment options
            click_button(driver, xpath="/html/body/div/div[3]/div/div/h4[2]")

            # "Spring over" button
            click_button(driver, class_name="button.link")

        else:
            raise NotImplementedError("Payment option must be one of [mobilepay, cash, skip].")

        wait_for_next_page(driver)
        assert "medlemskab er oprettet" in driver.page_source.lower()
