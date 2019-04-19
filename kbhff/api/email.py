import easyimap, email
from kbhff.api.exceptions import *
import time

def get_mail_credentials():
    try:
        # check if module exists:
        from kbhff.api.mail_credentials import mail_credentials
    except ModuleNotFoundError:
        # check if environment variables exist:
        from os import environ
        mail_credentials = {}
        # values will be None if environment variable doesn't exist
        mail_credentials["login"] = environ.get("MAIL_CREDENTIALS_EMAIL")
        mail_credentials["password"] = environ.get("MAIL_CREDENTIALS_PASSWORD")
    return mail_credentials
    
    
def get_gmail_connection(address = None, password = None):
    if address is None:
        address = get_mail_credentials()["login"]
    if password is None:
        password = get_mail_credentials()["password"]
    return easyimap.connect ('imap.gmail.com', address, password)

def get_latest_mail_to(to_address, email_connection = None, expect_title = None, retryCount = 0):
    """ Receive latest email sent to to_address.

    Optional parameters:
        expect_title --- if set, emails with titles that aren't an exact match will be ignored
        retry --- retry this many times with a second's delay each
    """
    assert retryCount >= 0

    connection_is_temporary = (email_connection is None)
    if connection_is_temporary:
        email_connection = get_gmail_connection()

    for i in range(0,1+retryCount):
        for mail in email_connection.listup(25):
            if mail.to == to_address and (expect_title in [mail.title, None]):
                if connection_is_temporary:
                    email_connection.quit()
                return mail
        time.sleep(1)

    if connection_is_temporary:
        email_connection.quit()
    raise NoEmailReceivedError(f"Found no Email to {to_address}.")

def get_activation_code_from_email(email_body):
    """ Parses body of the email sending an activation code and returns the code as string. """
    import re
    # some random assumptions on what codes look like have been made...
    # only lowercase letters or numbers
    # between 5 and 10 characters
    code_pattern_later = re.compile('ind i feltet:[ \r\n]{1,4}([a-z0-9]{5,10})[ \r\n]{1,4}Din konto vil blive')
    code_matches_later = code_pattern_later.findall(email_body)
    
    code_pattern_during_signup = re.compile('aktivere din konto:[ \r\n]{1,4}([a-z0-9]{5,10})[ \r\n]{1,4}Alternativt kan du klikke')
    code_matches_during_signup = code_pattern_during_signup.findall(email_body)
    
    code_matches = code_matches_later + code_matches_during_signup

    if len(code_matches) != 1:
        raise UnexpectedLayoutError(f"Could not find a unique activation code in the following mail body:\n {email_body}")
    return code_matches[0]
