import pytest

from navigation import *

@pytest.fixture(scope="module", params = [webdriver.Firefox, webdriver.Chrome] )
def driver(request):
    driver = (request.param)()
    yield driver # separates setup from teardown
    driver.close()

def test_cannotNavigateToGibberishPage(driver):
    with pytest.raises(PageNotImplementedError):
        navigate_to_page("gibberishPage", driver)
