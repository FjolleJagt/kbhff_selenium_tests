[![Build Status](https://travis-ci.com/cleborys/kbhff_selenium_tests.svg?branch=master)](https://travis-ci.com/cleborys/kbhff_selenium_tests)

# Integration Test of <pre-launch.kbhff.dk> using the Selenium Webdriver for Python

## Installation

 - (Optional) Add credentials for a gmail account in `kbhff/api/mail_credentials.py` as described below
 - Change to this directory and install this package (`kbhff`) via `pip install .`
 - Install the remaining requirements via `pip install -r requirements.txt`
 - Make sure you have installed `geckodriver` and `chromedriver` to user Firefox and Chrome with selenium
   - Download `geckodriver` version 0.24.0 `wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz`
   - Download `chromedriver` version 73.0` here: `wget https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_linux64.zip`
   - Unpack these into e.g. subdirectories named `geckodriver` and `chromedriver`
   - Add these subdirectories to your python path e.g. with `export PATH=$PATH:$PWD/geckodriver` and `export PATH=$PATH:$PWD/chromedriver`

## Email Credentials

There are two ways to use this package with a gmail account.
  1. Define two environment variables `MAIL_CREDENTIALS_EMAIL` containing your gmail address as string and `MAIL_CREDENTIALS_PASSWORD` containing the password to your account as string
  2. Add a `mail_credentilas.py` file to `kbhff/api/` as in the first installation step above. This file should define a `dict` called `mail_credentials` with keys `"login"` and `"password"` mapping your gmail address and its password as strings. Make sure to (re)install after adding this file.
