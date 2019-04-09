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
            self.current_url = "Mock_current_url"
            self.call_number = 0

        @property
        def page_source(self):
            self.call_number += 1
            return f"This is page_source call number {self.call_number}."

    driver = MockDriver()
    return driver

def test_cannotNavigateToGibberishPage(driver):
    with pytest.raises(PageNotImplementedError):
        navigate_to_page("gibberishPage", driver)

#def test_canNavigateToLogin(driver):
    #navigate_to_page("login", driver)
    #assert_text_on_page("text that should be on login page", driver, retry=3)

def test_assertTextRetriesIfNeeded(mock_driver_for_retries):
    mock_driver = mock_driver_for_retries
    with pytest.raises(TextNotFoundOnPageError):
        assert_text_on_page("call number 5", mock_driver, retry=3)
    assert "call number 5" in mock_driver.page_source

def test_assertTextDoesNotRetryIfUnnecessary(mock_driver_for_retries):
    mock_driver = mock_driver_for_retries
    assert_text_on_page("call number 1", mock_driver, retry=5)
    assert "call number 2" in mock_driver.page_source




