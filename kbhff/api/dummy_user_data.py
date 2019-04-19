user_data = {}
user_data["email"] = "cb.open.automail+dummyuser@gmail.com"
user_data["firstname"] = "Dummy"
user_data["lastname"] = "User"
user_data["password"] = "dummyPassword"
user_data["department"] = "Vesterbro"

if __name__ == "__main__":
    from kbhff.api.signup import *
    print("Creating dummy user with fixed details.")
    signup_via_webform(user_data)
