from cpapi import APIClient, APIClientArgs
import json
import random
import string
import pandas as pd

# Publish the session to the SMS
def publish(client):
    response = client.api_call("publish", {})
    response_logger(response, "Session published successfully.")


# Checks if the response is
# successful or not
def response_logger(response, successMessage):
    if response.success:
        if successMessage is not None:
            print(successMessage)
        return True
    else:
        raise Exception(response.error_message)


# Creates a user and returns
# it uid
def create_user(client, name, password):
    response = client.api_call(
        "add-generic-object",
        {
            "name": name,
            "create": "com.checkpoint.objects.classes.dummy.CpmiUser",
            "authMethod": "INTERNAL_PASSWORD",
            "internalPassword": password,
        },
    )

    if response_logger(response, None):
        jsondata = json.loads(json.dumps(response.data))
        return jsondata["uid"]


# Creates a user group and returns its uid
def create_group(client, name):
    response = client.api_call(
        "add-generic-object",
        {"name": name, "create": "com.checkpoint.objects.classes.dummy.CpmiUserGroup"},
    )

    if response_logger(response, None):
        jsondata = json.loads(json.dumps(response.data))
        return jsondata["uid"]


# Check if user already exists
# If user exists, return uid
# If not, create user and return uid
def get_user(client, name, password):

    response = client.api_call("show-generic-objects", {"name": name},)

    isSuccess = response_logger(response, "searching for user {}".format(name))

    if isSuccess:
        jsondata = json.loads(json.dumps(response.data))

        if len(jsondata["objects"]) == 0:
            # Create user
            return create_user(client, name, password)
        else:
            return retrieve_uid_from_array(jsondata)


# Check if group already exists
# If group exists, return uid
# If not, create group and return uid
def get_group(client, name):
    response = client.api_call("show-generic-objects", {"name": name},)

    isSuccess = response_logger(response, "searching for group {}".format(name))

    if isSuccess:
        jsondata = json.loads(json.dumps(response.data))

        if len(jsondata["objects"]) == 0:
            # Create group
            return create_group(client, name)
        else:
            return retrieve_uid_from_array(jsondata)


# Retrieve uid from array
def retrieve_uid_from_array(jsondata):
    for i in range(len(jsondata["objects"])):
        obj = jsondata["objects"][i]
        return obj["uid"]


# Assigns user to group
def assign_user_to_group(client, uuid, guid):
    response = client.api_call(
        "set-generic-object", {"uid": guid, "emptyFieldName": {"add": uuid}}
    )
    response_logger(response, "User has been added to group")


# Generate password from email
def generate_password(email):
    password = email[0:3]
    password = (
        password
        + str(random.choice(string.digits))
        + str(random.choice(string.digits))
        + str(random.choice(string.digits))
        + str(random.choice(string.punctuation))
    )
    return password


# Extract the user name from email
def generate_user_name(email):
    return email.split("@")[0]


def main():

    try:
        # Read from file
        dataframe = pd.read_excel("User-Mobility-Test.xlsx")
        dataframe_username = pd.DataFrame(dataframe, columns=["User Name"])
        dataframe_email = pd.DataFrame(dataframe, columns=["User Email"])
        dataframe_groups = pd.DataFrame(dataframe, columns=["Groups"])

        # SMS Credentials
        sms_ip = "172.17.168.101"
        sms_username = "test2"
        sms_password = "1234"

        # Initialize the SMS session
        client_args = APIClientArgs(server=sms_ip, api_version=1.1)

        with APIClient(client_args) as client:
            # Login to server:
            login_res = client.login(sms_username, sms_password)

            # If login is not successful, print the error message.
            if login_res.success is False:
                raise Exception(
                    "Login failed. Please check SMS version (this script works only with R80.xx)"
                )
            else:
                print("Successfully connected to: {}".format(sms_ip))

                for index, row in dataframe.iterrows():
                    # User & Group Data
                    groups = (row["Groups"]).split(";")
                    user_email = row["User Email"]
                    user_name = generate_user_name(user_email)
                    user_password = generate_password(user_email)

                    # Get the user uid
                    uuid = get_user(client, user_name, user_password)

                    # iterate through all groups
                    for i in range(len(groups)):
                        group = groups[i]

                        # Get the group uid
                        guid = get_group(client, group)

                        # Assign the user to group
                        assign_user_to_group(client, uuid, guid)

                # Publish the session
                publish(client)

    except Exception as e:
        print("An internal error occurred. Error: {}".format(e))
        exit(1)


if __name__ == "__main__":
    main()
