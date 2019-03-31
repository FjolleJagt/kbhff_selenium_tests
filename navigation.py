import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

pages = {}
pages["root"] = "http://kbhff.local/"
pages["root"] = "pre-launch.kbhff.dk/"
pages["login"] = pages["root"] + "login"
pages["signup"] = pages["root"] + "bliv-medlem"

def navigate_to_page(page_name, driver):
    """Navigate to the specified page.

    Positional arguments:
        page_name -- a string corresponding to the desired page. Supported values are:
            login
            bekraeft_konto
            opret_adgangskode
            bekraeft_konto_receipt: /bliv-medlem/bekraeft/kvittering
            signup
        driver -- the Selenium driver to use
    page names not yet implementer:
        bekraeft_konto
        opret_adgangskode
        bekraeft_konto_receipt: /bliv-medlem/bekraeft/kvittering
    """

    if page_name in pages:
        driver.get(pages[page_name])
        # wait for driver to start loading next page
        time.sleep(0.5)
        # wait for page to load, up to ten seconds
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))
    else:
        raise NotImplementedError("{page_name} is not a known page name. \
                Known page names are {known}".format(\
                page_name = page_name,
                known = ", ".join(pages.keys()))
                )

def navigate_to_link(link, driver):
    """Navigates to specified URL."""
    driver.get(link)
    # wait for driver to start loading next page
    time.sleep(0.5)
    # wait for page to load, up to ten seconds
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))

def find_form_field(driver, form_id=None, class_name=None):
    """Returns a field in the first form that appears on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    Named arguments:
        form_id -- the id of the form input to fill
        class_name -- a CSS class of the form input to fill. If multiple form fields share the same class, then the first field that has the class is used.

    It is compulsory to specify precisely one of id and className, otherwise the function will raise an InvalidArgumentsError"""
    if (form_id == None and class_name == None) or (form_id != None and class_name != None):
        raise InvalidArgumentError("Precisely one of form_id and class_name has to be specified".)
    elif (form_id != None):
        entry_field = driver.find_element_by_id(form_id)
    elif (class_name != None):
        entry_field = driver.find_element_by_class_name(class_name)

    return entry_field

def fill_form_field(value, driver, form_id=None, class_name=None):
    """Fill out a field in the first form that appears on the current page.

    Positional arguments:
        value -- a string whose contents should be entered into the form field
        driver -- the Selenium driver to use

    Named arguments:
        form_id -- the id of the form input to fill
        class_name -- a CSS class of the form input to fill. If multiple form fields share the same class, then the first field that has the class is used.

    It is compulsory to specify precisely one of id and className, otherwise the function will raise an InvalidArgumentsError"""
    entry_field = find_form_field(driver, form_id=form_id, class_name = class_name)
    entry_field.send_keys(value)

def get_form_field(driver, form_id=None, className=None):
    """Return the current value of a field in the first form that appears on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    Named arguments:
        form_id -- the id of the form input whose value to return
        className -- a CSS class of the form input whose value to return. If multiple form fields share the same class, then the first field that has the class is used.

    It is compulsory to specify precisely one of form_id and className, otherwise the function will raise an InvalidArgumentsError"""
    field = find_form_field(driver, form_id=form_id, class_name = class_name)
    return field.getAttribute("value")

def submit_form(driver):
    """Click submit button on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    The function will attempt to find a submit button to click; if unable to find one, it will raise an UnexpectedLayoutError."""
    # This raises something like "NoSuchElementError" if unable to find one
    submit_button = driver.find_element_by_id("submit")
    submit_button.click()


def try_login(driver, username, password):
    driver.get(pages["login"])

    login_url = driver.current_url

    username_entry = driver.find_element_by_id("input_username")
    username_entry.send_keys(username)

    password_entry = driver.find_element_by_id("input_password")
    password_entry.send_keys(password)
    password_entry.submit()
    
    # wait for driver to start loading next page
    time.sleep(0.5)
    # wait for page to load, up to ten seconds
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))

def request_password_reset(driver, user_email):
    driver.get(pages["login"])

    forgot_password_link = driver.find_element_by_xpath("//p[@class='forgot']/a")
    forgot_password_link.click()

    WebDriverWait(driver, 10).until(EC.url_changes(pages["login"]))

    email_entry = driver.find_element_by_id("input_username")
    email_entry.send_keys(user_email)
    email_entry.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_reset-token")))

    # wait for token to be written to database
    time.sleep(0.5) 

def enter_password_request_token(driver, reset_token):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_reset-token")))

    reset_token_entry = driver.find_element_by_id("input_reset-token")
    reset_token_entry.send_keys(reset_token)
    reset_token_entry.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_new_password")))

def enter_new_password_for_reset(driver, new_password):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_new_password")))
    password_entry = driver.find_element_by_id("input_new_password")
    password_entry.send_keys(new_password)

    password_confirm = driver.find_element_by_id("input_confirm_password")
    password_confirm.send_keys(new_password)
    password_confirm.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input_username")))

