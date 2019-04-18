import pytest
from fixtures import *

from navigation import *
from webpage_patterns import *

import time


# Test specification number 1
def test_unverifiedUserFirstLogin(driver, unverified_user_via_medlemshjaelp):
    user = unverified_user_via_medlemshjaelp

    try_login(driver, user["email"], user["password"])
    verify_account_on_first_login(user["email"], driver)
    create_password(user["password"], driver)

    assert_current_page_is("kvittering", driver)

    navigate_to_page("login", driver)
    assert_current_page_is("login", driver)
    assert get_form_field_value(driver, form_id="input_username") == user["email"]



