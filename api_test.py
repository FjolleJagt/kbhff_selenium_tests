import pytest

from navigation import *

def test_cannotNavigateToGibberishPage():
    with pytest.raises(NotImplementedError):
        with webdriver.Firefox() as driver:
            navigate_to_page("gibberishPage", driver)
