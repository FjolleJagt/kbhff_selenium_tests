import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from custom_exceptions import *

pages = {}
pages["root"] = "http://kbhff.local/"
pages["root"] = "http://pre-launch.kbhff.dk/"
pages["login"] = pages["root"] + "login"
pages["signup"] = pages["root"] + "bliv-medlem"
pages["min_side"] = pages["root"] + "profil"
pages["medlemshjaelp"] = pages["root"] + "medlemshjaelp"
pages["medlemshjaelp-signup"] = pages["medlemshjaelp"] + "/tilmelding"

def navigate_to_page(page_name, driver):
    """Navigate to the specified page.

    Positional arguments:
        page_name -- a string corresponding to the desired page. See supported values in code.
        driver -- the Selenium driver to use
    """

    if page_name in pages:
        driver.get(pages[page_name])
        # wait for driver to start loading next page
        time.sleep(0.5)
        # wait for page to load, up to ten seconds
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))
    else:
        raise PageNotImplementedError(page_name, pages)

def navigate_to_link(link, driver):
    """Navigates to specified URL."""
    driver.get(link)
    # wait for driver to start loading next page
    time.sleep(0.5)
    # wait for page to load, up to ten seconds
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))

def assert_current_page_is(page_name, driver):
    if page_name in pages:
        assert driver.current_url == pages[page_name]
    else:
        raise PageNotImplementedError(page_name, pages)

def find_form_field(driver, form_id=None, class_name=None):
    """Returns a field in the first form that appears on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    Named arguments:
        form_id -- the id of the form input to fill
        class_name -- a CSS class of the form input to fill. If multiple form fields share the same class, then the first field that has the class is used.

    It is compulsory to specify precisely one of id and className, otherwise the function will raise an InvalidArgumentsError"""
    if (form_id is None and class_name is None) or (form_id is not None and class_name is not None):
        raise InvalidArgumentError("Precisely one of form_id and class_name has to be specified.")
    elif (form_id != None):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, form_id)))
        entry_field = driver.find_element_by_id(form_id)
    elif (class_name != None):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
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

    It is compulsory to specify precisely one of form_id and class_name, otherwise the function will raise an InvalidArgumentsError"""
    entry_field = find_form_field(driver, form_id=form_id, class_name = class_name)
    entry_field.send_keys(value)

def get_form_field_value(driver, form_id=None, className=None):
    """Return the current value of a field in the first form that appears on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    Named arguments:
        form_id -- the id of the form input whose value to return
        className -- a CSS class of the form input whose value to return. If multiple form fields share the same class, then the first field that has the class is used.

    It is compulsory to specify precisely one of form_id and className, otherwise the function will raise an InvalidArgumentsError"""
    field = find_form_field(driver, form_id=form_id, class_name = class_name)
    return field.getAttribute("value")

def find_button(driver, button_id=None, class_name=None, xpath=None):
    """Returns the first matching button on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    Named arguments:
        button_id -- the id of the button to be returned
        class_name -- a CSS class of the button to be returned. If multiple form fields share the same class, then the first field that has the class is used.
        xpath -- XPath of the element to be returned.

    It is compulsory to specify precisely one of button_id and class_name, otherwise the function will raise an InvalidArgumentsError"""
    if not ((button_id is not None) ^ (class_name is not None) ^ (xpath is not None)):
        raise InvalidArgumentError("Precisely one of button_id, class_name, or xpath has to be specified.")
    elif (button_id is not None):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, button_id)))
        button = driver.find_element_by_id(button_id)
    elif (class_name is not None):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        button = driver.find_element_by_class_name(class_name)
    elif (xpath is not None):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
        button = driver.find_element_by_xpath(xpath)

    return button

def click_button(driver, button_id=None, class_name=None, xpath=None):
    """Locates and clicks a button on the current page by id of class name.
    Raises NoSuchElementError, if unable to find an element as specified."""
    button = find_button(driver, button_id=button_id, class_name=class_name, xpath=xpath)
    button.click()

def submit_form(driver):
    """Click submit button on the current page.

    Positional arguments:
        driver -- the Selenium driver to use

    The function will attempt to find a submit button to click; if unable to find one, it will raise an UnexpectedLayoutError."""
    # Might want to add other options than button.primary.clickable later
    click_button(driver, class_name="button.primary.clickable")


def select_from_dropdown(option_text, driver, dropdown_id):
    """Attempts to find dropdown menu and select specified option.

    Positional arguments:
        driver -- the Selenium driver to use
        dropdown_id -- the id of the dropdown menu
        option_text -- the text of the dropdown item to be selected
    """
    dropdown_menu = Select(driver.find_element_by_id(dropdown_id))
    dropdown_menu.select_by_visible_text(option_text)

def check_checkbox(driver, box_id, should_end_up_selected = True):
    """Interacts with a checkbox, will tick the box by default.

    Positional arguments:
        driver -- the Selenium driver to use
        box_id -- the id of the checkbox
    Optional arguments:
        should_end_up_selected -- box will end up ticked if True, else unticked. Default True.
    """
    checkbox = driver.find_element_by_id(box_id)
    if checkbox.get_attribute("type") != "checkbox":
        raise UnexpectedLayoutError(f"The element with id {box_id} is not a checkbox.")
    if checkbox.is_selected() != should_end_up_selected:
        checkbox.click()


def wait_for_next_page(driver):
    # wait for driver to start loading next page
    time.sleep(0.5)
    # wait for page to load, up to ten seconds
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//html")))


def try_login(driver, username, password):
    """ Tries to log in with given credentials. """
    navigate_to_page("login", driver)

    fill_form_field(username, driver, "input_username")
    fill_form_field(password, driver, "input_password")
    submit_form(driver)

    wait_for_next_page(driver)

def login(driver, username, password):
    """ Like try_login but throws error if the user could not be logged in regularly."""
    try_login(driver, username, password)
    try:
        assert_current_page_is("min_side", driver)
    except AssertionError:
        raise InvalidUserError(f"Could not log in with username {username} and password {password} and reach 'Min Side'. Make sure the user exists and is activated.")

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
