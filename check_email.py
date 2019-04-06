import easyimap, email
from mail_credentials import *
from custom_exceptions import *

def get_latest_mail_to(to_address):
    gmail = easyimap.connect('imap.gmail.com', mail_credentials["login"], \
            mail_credentials["password"])
    for mail_id in gmail.listids():
        mail = gmail.mail(mail_id)
        if mail.to == to_address:
            return mail

    raise NoEmailReceivedError(f"Found no Email to {to_address}.")

def get_activation_code_from_email(email_body):
    """ Parses body of the email sending an activation code and returns the code as string. """
    import re
    # some random assumptions on what codes look like have been made...
    # only lowercase letters or numbers
    # between 5 and 10 characters
    code_pattern_later = re.compile('ind i feltet:\s{1,4}([a-z0-9]{5,10})\s{1,4}Din konto vil blive')
    code_matches_later = code_pattern_later.findall(email_body)
    
    code_pattern_during_signup = re.compile('aktivere din konto:\s{1,4}([a-z0-9]{5,10})\s{1,4}Alternativt kan du klikke')
    code_matches_during_signup = code_pattern_during_signup.findall(email_body)
    
    code_matches = code_matches_later + code_matches_during_signup

    assert len(code_matches) == 1
    return code_matches[0]

if __name__ == "__main__":
    mail = get_latest_mail_to("cb.open.automail@gmail.com")
    print(mail.title)



