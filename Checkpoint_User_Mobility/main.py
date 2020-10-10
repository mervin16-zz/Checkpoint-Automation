from cpapi import APIClient, APIClientArgs
import json
import pandas as pd
from user import User

# FIXME("Remove when done with project")
import traceback

# Data that should be moved to a file
# SMS Credentials
sms_ip = "172.30.43.150"
sms_username = "api"
sms_password = "ptc686grt09"
api_version = 1.1


###################################
############ Constants ############
###################################
# Available Actions
ACTION_ADD = "ADD"
ACTION_DELETE = "DELETE"
ACTION_EDIT = "EDIT"


######################################
############ My Functions ############
######################################

# Displays a message
def display(message):
    # TODO("Use a logger instead of print")
    print(message)


# Publish the session to the SMS
def publish(client):
    response = client.api_call("publish", {})
    response_logger(response, "Session published successfully.")


# Discard the session from the SMS
def discard(client):
    response = client.api_call("discard", {})
    response_logger(response, "Session has been discarded.")


# Checks if the response is
# successful or not
def response_logger(response, successMessage):
    if response.success:
        if successMessage is not None:
            display(successMessage)
        return True
    else:
        raise Exception(response.error_message)


# Deletes a user
def delete_user(client, uid, name):
    response = client.api_call("delete-generic-object", {"uid": uid})
    response_logger(response, "The user {} has been deleted".format(name))


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


def get_user(client, name, password):
    # Check if user already exists
    # If user exists, return uid
    # If not, create user and return uid
    response = client.api_call("show-generic-objects", {"name": name},)

    isSuccess = response_logger(response, "Processing user {}".format(name))

    if isSuccess:
        jsondata = json.loads(json.dumps(response.data))

        if len(jsondata["objects"]) == 0:
            # Create user
            return create_user(client, name, password)
        else:
            # Return uid of existing user
            return retrieve_uid_from_array(jsondata)


def get_group(client, name):
    # Check if group already exists
    # If group exists, return uid
    # If not, create group and return uid
    response = client.api_call("show-generic-objects", {"name": name},)

    isSuccess = response_logger(response, "Processing the group {}".format(name))

    if isSuccess:
        jsondata = json.loads(json.dumps(response.data))

        if len(jsondata["objects"]) == 0:
            # Create group
            return create_group(client, name)
        else:
            # Return existing group
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


# Check action
def action_checker(client, user):
    if user.action.upper() == ACTION_ADD.upper():
        # Get the user uid
        uuid = get_user(client, user.name, user.password)

        # iterate through all groups
        for i in range(len(user.groups)):
            # get group name individually
            group = user.groups[i]

            # If group name is NOT empty
            # we continue the assignment
            if group != "":
                # Get the group uid
                guid = get_group(client, group)

                # Assign the user to group
                assign_user_to_group(client, uuid, guid)
    elif user.action.upper() == ACTION_DELETE.upper():
        # FIXME("If user doesn't exists it will create it")
        uid = get_user(client, user.name, user.password)
        delete_user(client, uid, user.name)
    elif user.action.upper() == ACTION_EDIT.upper():
        display("Action is edit")
    else:
        raise Exception(
            "Action entered is misleading. Please enter the correct actions and try again."
        )


#####################################
########### Main Function ###########
#####################################
def main():

    # Try / Catch to get exceptions regarding
    # excel file connections and
    # checkpoint api client initialization
    try:

        # Read data from file
        # TODO("file path should be in settings json")
        dataframe = pd.read_excel("Checkpoint_User_Mobility/User-Mobility-Test.xlsx")
        # Since blank cells return 'nan' instead of empty string
        # we replace all 'nan' with an empty string
        dataframe = dataframe.fillna("")

        # Initialize the SMS session
        client_args = APIClientArgs(server=sms_ip, api_version=api_version)

        with APIClient(client_args) as client:

            # Try / Catch to get exceptions regarding
            # all checkpoint operations
            try:
                # Login to server:
                login_res = client.login(sms_username, sms_password)

                # If login is not successful, log the error message.
                if login_res.success is False:
                    raise Exception(
                        "Login failed. Please check SMS version (this script works only with R80.xx)"
                    )
                else:
                    display("Successfully connected to: {}".format(sms_ip))

                    # Iterate through each row
                    # in the excel table
                    # Index is not used here but should
                    # NOT BE REMOVED
                    for index, row in dataframe.iterrows():

                        # Filter data in excel
                        # data filtered are user email, groups assigned and
                        # action need to be taken
                        groups = str(row["Groups"]).split(";")
                        user_email = row["User Email"]
                        action = row["Action"]
                        # user_name = generate_user_name(user_email)
                        # user_password = generate_password(user_email)

                        # Create a User object
                        user = User(user_email, groups, action)

                        # This is the main function which
                        # handles all the logic
                        # Checks the action and determines
                        # which functions to call
                        action_checker(client, user)

                    # If everything worked
                    # publish the session to the SMS
                    publish(client)

            except Exception as e:
                # Prints the error message
                # and starts discarding the session
                display("An internal error occurred. Error: {}".format(e))
                display("Discarding the session...")

                # Discard the active session
                discard(client)

                # FIXME("Remove when done with project")
                traceback.print_exc()
                exit(1)

    except Exception as e:
        # Prints the error message
        display("An internal error occurred. Error: {}".format(e))

        # FIXME("Remove when done with project")
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
