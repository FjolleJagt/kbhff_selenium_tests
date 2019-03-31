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

if __name__ == "__main__":
    mail = get_latest_mail_to("cb.open.automail@gmail.com")
    print(mail.title)



