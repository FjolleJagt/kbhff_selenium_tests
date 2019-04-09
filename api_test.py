import pytest

from navigation import *

@pytest.fixture(scope="function", params = [webdriver.Firefox, webdriver.Chrome] )
def driver(request):
    driver = (request.param)()
    yield driver # separates setup from teardown
    driver.close()

@pytest.fixture(scope="function")
def mock_driver_for_retries():
    class MockDriver:
        def __init__(self):
            self.call_number_source = 0
            self.call_number_url = 0

        @property
        def page_source(self):
            self.call_number_source += 1
            return f"This is page_source call number {self.call_number_source}."

        @property
        def current_url(self):
            self.call_number_url += 1
            return f"This is current_url call number {self.call_number_url}."

    driver = MockDriver()
    return driver

def test_cannotNavigateToGibberishPage(driver):
    with pytest.raises(PageNotImplementedError):
        navigate_to_page("gibberishPage", driver)

def test_canNavigateToLogin(driver):
    navigate_to_page("login", driver)
    assert_text_on_page("Velkommen indenfor", driver, retry=3)

def test_assertTextRetriesIfNeeded(mock_driver_for_retries):
    mock_driver = mock_driver_for_retries
    with pytest.raises(TextNotFoundOnPageError):
        assert_text_on_page("call number 5.", mock_driver, retry=3)
    assert "call number 5." in mock_driver.page_source

def test_assertTextDoesNotRetryIfUnnecessary(mock_driver_for_retries):
    mock_driver = mock_driver_for_retries
    assert_text_on_page("call number 1.", mock_driver, retry=5)
    assert "call number 2." in mock_driver.page_source

def test_assertCurrentPageRetriesIfNeeded(mock_driver_for_retries):
    mock_driver = mock_driver_for_retries
    global pages
    pages["call 5"] = "This is current_url call number 5."
    with pytest.raises(EndedUpOnWrongPageError):
        assert_current_page_is("call 5", mock_driver, retry=3)
    assert "call number 6." in mock_driver.current_url #account for one more call in error message

def test_assertCurrentPageDoesNotRetryIfUnnecessary(mock_driver_for_retries):
    mock_driver = mock_driver_for_retries
    global pages
    pages["call 1"] = "This is current_url call number 1."
    assert_current_page_is("call 1", mock_driver, retry=5)
    assert "call number 2." in mock_driver.current_url

def test_canFillAndReadFormField(driver):
    navigate_to_page("login", driver)
    input_string = "test input with weird symbols 21830<><=/|\\@'$ø"
    fill_form_field(input_string, driver, form_id="input_username")
    read_string = get_form_field_value(driver, form_id="input_username")
    assert input_string == read_string
