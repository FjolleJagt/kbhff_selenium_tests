Some notes on setup:

- `mail_credentials`: currently an email is hardcoded, but not included in repository. To set the email either add a `kbhff/api/mail_credentials.py` file defining a dict called `mail_credentials` with keys `"login"` and `"password"`, where both values are strings giving the credentials of your gmail address or define two environment variables named `MAIL_CREDENTIALS_EMAIL` and `MAIL_CREDENTIALS_PASSWORD` instead.

- make sure you have the geckodriver for Firefox and the chrome driver.

