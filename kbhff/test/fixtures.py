import pytest

from kbhff.api.navigation import *
from kbhff.api.signup import *
from kbhff.api.dummy_user_data import user_data as permanent_user
from kbhff.api.delete_user import *

from pyvirtualdisplay import Display

@pytest.fixture(scope="function", params = [webdriver.Firefox, webdriver.Chrome] )
def driver(request):
    display = Display(visible=0, size=(1920,1080))
    display.start()
    driver = (request.param)()
    yield driver # separates setup from teardown
    driver.close()
    display.stop()

@pytest.fixture(scope="function")
def unverified_user_via_medlemshjaelp():
    user_data = random_user_data()
    signup_via_medlemshjaelp(permanent_user, user_data)
    yield user_data
    delete_user(user_data)

@pytest.fixture(scope="function")
def unverified_user_via_webform():
    user_data = random_user_data()
    signup_via_webform(user_data, activate_right_away=False)
    yield user_data
    delete_user(user_data)

