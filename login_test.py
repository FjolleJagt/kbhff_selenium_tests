import pytest
from fixtures import *

from navigation import *

import time


# Test specification number 1
def test_unverifiedUserFirstLogin(driver, unverified_user_via_medlemshjaelp):
    user = unverified_user_via_medlemshjaelp

    try_login(driver, user["email"], user["password"])
    assert_current_page_is("bekraeft_konto", driver)

#    fill_form_field(verification_code, driver, form_id="input_FIELD")
#    submit_form(driver)
#    assert_current_page_is("opret_adgangskode", driver)

#    fill_form_field(user["password"], driver, form_id="input_password")
#    fill_form_field(user["password"], driver, form_id="input_confirm_password")
#    assert_current_page_is("kvittering", driver)

#    click_link("login")
#    assert_current_page_is("login", driver)
#    assert get_form_field_value(driver, form_id="input_FIELD") == user["email"]



