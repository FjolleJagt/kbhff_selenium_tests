from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

pages = {}
pages["root"] = "http://kbhff.local/"
pages["login"] = pages["root"] + "login"

def test_cantLoginWithBadCredentials():
	driver = webdriver.Firefox()
	driver.get(pages["login"])

	username_entry = driver.find_element_by_id("input_username")
	username_entry.send_keys("dont@email.me")

	password_entry = driver.find_element_by_id("input_password")
	password_entry.send_keys("thatsnotmypassword")
	password_entry.submit()

#wait until the error message appears, or 10 seconds, whichever is longer
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class='error']")))

	assert "forkert brugernavn eller password" in driver.page_source

	driver.quit()
