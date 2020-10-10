import json


class Settings:

    # Initialize the Settings class
    def __init__(self):
        with open("Checkpoint_User_Mobility/config/settings.json") as json_file:
            settings = json.load(json_file)

            # SMS settings
            self.sms_ip = settings["sms"]["host"]
            self.sms_username = settings["sms"]["username"]
            self.sms_password = settings["sms"]["password"]

            # API settings
            self.api_version = settings["api"]["version"]

            # User data settings
            self.user_data_path = settings["user_data"]["path"]
