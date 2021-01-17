import random
import string


class User:

    # Initialize the user class
    def __init__(self, email, groups, action):
        self.email = email
        self.groups = groups
        self.action = action
        self.name = self.generate_user_name()
        self.password = self.generate_password()

    # Generate password from email
    def generate_password(self):
        password = self.email[0:3]
        password = (
            password
            + str(random.choice(string.digits))
            + str(random.choice(string.digits))
            + str(random.choice(string.digits))
            + str(random.choice(string.punctuation))
        )
        return password

    # Extract the user name from email
    def generate_user_name(self):
        return self.email.split("@")[0]
