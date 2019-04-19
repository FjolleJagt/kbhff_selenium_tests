import easyimap, email
from kbhff.api.mail_credentials import *
from kbhff.api.exceptions import *
import time

def get_latest_mail_to(to_address, expect_title=None, retryCount=0):
    """ Receive latest email sent to to_address.

    Optional parameters:
        expect_title --- if set, emails with titles that aren't an exact match will be ignored
        retry --- retry this many times with a second's delay each
    """
    assert retryCount >= 0

    for i in range(0,1+retryCount):
        gmail = easyimap.connect('imap.gmail.com', mail_credentials["login"], \
                mail_credentials["password"])
        for mail_id in gmail.listids():
            mail = gmail.mail(mail_id)
            if mail.to == to_address and (expect_title in [mail.title, None]):
                return mail
        time.sleep(1)

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
