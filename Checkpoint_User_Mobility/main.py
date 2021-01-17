from cpapi import APIClient, APIClientArgs
from datetime import datetime
from passlib.hash import des_crypt
import pandas as pd
import enum
import os
from models.user import User
from utils.settings import Settings
import utils.constants as Const
from utils.utils import create_logger

######################################
############ Enumerators ############
######################################
class Action(enum.Enum):
    ADD = 1
    DELETE = 2
    EDIT = 3


######################################
########## Global Variables ##########
######################################
logger = None

######################################
############ My Functions ############
######################################
def display(message):
    # Logs a message
    logger.info(message)


def publish(client):
    # Publish the session to the SMS
    response = client.api_call("publish", {})
    response_logger(response, Const.MESSAGE_SESSION_PUBLISHED)


def discard(client):
    # Discard the session from the SMS
    response = client.api_call("discard", {})
    response_logger(response, Const.MESSAGE_SESSION_DISCARDED)


def hash_user_password(password):
    return des_crypt.hash(password)


def response_logger(response, successMessage):
    # Checks if the response is
    # successful or not
    if response.success:
        if successMessage is not None:
            display(successMessage)
        return True
    else:
        raise Exception(response.error_message)


def delete_user(client, uid, name):
    response = client.api_call("delete-generic-object", {"uid": uid})
    response_logger(response, Const.MESSAGE_USER_REMOVED.format(name))


def create_user(client, name, password):
    # Creates a user and returns
    # its uid
    response = client.api_call(
        "add-generic-object",
        {
            "name": name,
            "create": "com.checkpoint.objects.classes.dummy.CpmiUser",
            "authMethod": "INTERNAL_PASSWORD",
            "internalPassword": hash_user_password(password),
        },
    )

    if response_logger(response, None):
        # We display the password generated for the user
        display(Const.MESSAGE_USER_PASSWORD_GENERATED.format(password))

        return response.data["uid"]


def create_group(client, name):
    # Creates a user group and returns its uid
    response = client.api_call(
        "add-generic-object",
        {"name": name, "create": "com.checkpoint.objects.classes.dummy.CpmiUserGroup"},
    )

    if response_logger(response, None):
        return response.data["uid"]


def get_user_data(client, name):
    # This functions checks if the user
    # exists or not
    response = client.api_call("show-objects", {"filter": name},)

    isSuccess = response_logger(response, Const.MESSAGE_USER_PROCESSING.format(name))

    if isSuccess:
        # Returns a list of objects
        return response.data["objects"]
    else:
        raise Exception(Const.ERROR_USER_FETCHING.format(name))


def get_user(client, name, password):
    # Check if user already exists
    # If user exists, return uid
    # If not, create user and return uid
    objects = get_user_data(client, name)

    # Filter the objects by CpmiUsers and the exact user name
    # return the next one
    filter_by_type = filter(lambda d: d["type"] == "CpmiUser", objects)
    filter_by_name = next(filter(lambda d: d["name"] == name, filter_by_type), None)

    if filter_by_name is None:
        # Create user
        return create_user(client, name, password)
    else:
        # Return uid of existing user
        return filter_by_name["uid"]


def get_group_data(client, name):
    # This functions checks if the group
    # exists or not
    response = client.api_call("show-objects", {"filter": name},)

    isSuccess = response_logger(response, Const.MESSAGE_GROUP_PROCESSING.format(name))

    if isSuccess:
        # Returns a list of objects
        return response.data["objects"]
    else:
        raise Exception(Const.ERROR_GROUP_FETCHING.format(name))


def get_group(client, name):
    # Check if group already exists
    # If group exists, return uid
    # If not, create group and return uid

    objects = get_group_data(client, name)

    # Filter the objects by user groups only and
    # return the next one
    filtered = next(filter(lambda d: d["type"] == "CpmiUserGroup", objects), None)

    if filtered is None:
        # Create group
        return create_group(client, name)
    else:
        # Return existing group
        return filtered["uid"]


def assign_user_to_group(client, uuid, guid):
    # Assigns user to group
    response = client.api_call(
        "set-generic-object", {"uid": guid, "emptyFieldName": {"add": uuid}}
    )
    response_logger(response, Const.MESSAGE_USER_ADDED_TO_GROUP)


def remove_user_from_group(client, uuid, guid):
    # Removes user from group
    response = client.api_call(
        "set-generic-object", {"uid": guid, "emptyFieldName": {"remove": uuid}}
    )
    response_logger(response, Const.MESSAGE_USER_REMOVED_FROM_GROUP)


def action_add(client, user):
    # Get the user uid
    uuid = get_user(client, user.name, user.password)

    # iterate through all groups
    for group in user.groups:
        # get group name individually
        # removes all whitespaces as not allowed in checkpoint for User groups
        group = group.replace(" ", "")

        # If group name is NOT empty
        # we continue the assignment
        if group != "":
            # Get the group uid
            guid = get_group(client, group)

            # Assign the user to group
            assign_user_to_group(client, uuid, guid)


def action_delete(client, user):
    # Returns the json data of the user
    users = get_user_data(client, user.name)

    # Filter the objects by CpmiUsers and the exact user name
    # return the next one
    filter_by_type = filter(lambda d: d["type"] == "CpmiUser", users)
    filter_by_name = next(
        filter(lambda d: d["name"] == user.name, filter_by_type), None
    )

    # If no objects returned
    # user doesn't exist, thefore we don't enter if
    if filter_by_name is not None:
        delete_user(client, filter_by_name["uid"], user.name)


def action_edit(client, user):
    # iterate through all groups
    for group in user.groups:
        # get group name individually
        # removes all whitespaces as not allowed in checkpoint for User groups
        group = group.replace(" ", "")

        # Returns the json data of the group
        groups = get_group_data(client, group)

        # Filter the objects by user groups only and
        # return the next one
        filtered = next(filter(lambda d: d["type"] == "CpmiUserGroup", groups), None)

        # If no objects returned
        # group doesn't exist, thefore we don't enter if
        if filtered is not None:
            # Get the user uid
            uuid = get_user(client, user.name, user.password)
            guid = filtered["uid"]

            remove_user_from_group(client, uuid, guid)


def action_checker(client, user):
    # Checks which action is associated to the
    # user and calls the correct functions accordingly
    if user.action.upper() == Action.ADD.name:
        action_add(client, user)
    elif user.action.upper() == Action.DELETE.name:
        action_delete(client, user)
    elif user.action.upper() == Action.EDIT.name:
        action_edit(client, user)
    else:
        raise Exception(Const.ERROR_ACTION_MISLEADING.format(user.action, user.name))


def install_policy(client, settings):
    # Install the policy on the SMS
    display(Const.MESSAGE_POLICY_INSTALLING)

    response = client.api_call(
        "install-policy",
        {"policy-package": settings.sms_policy, "targets": settings.sms_gateways},
    )

    response_logger(response, Const.MESSAGE_POLICY_INSTALLED)


def logger_config():
    global logger
    # log folder path
    LOG_FOLDER = os.path.join(os.path.dirname(__file__), "log/")

    # create log folder
    if os.path.exists(LOG_FOLDER) is False:
        os.mkdir(LOG_FOLDER)

    logger = create_logger(
        (LOG_FOLDER + datetime.now().strftime("%Y-%m-%d--%H-%M-%S") + ".log")
    )


#####################################
########### Main Function ###########
#####################################
def main():

    # Try / Catch to get exceptions regarding
    # excel file connections and
    # checkpoint api client initialization
    try:

        # Logger configurations
        logger_config()

        # Get settings from Settings class
        settings = Settings()

        # Read data from file
        dataframe = pd.read_excel(settings.user_data_path)
        # Since blank cells return 'nan' instead of empty string
        # we replace all 'nan' with an empty string
        dataframe = dataframe.fillna("")

        # Initialize the SMS session
        client_args = APIClientArgs(
            server=settings.sms_ip, api_version=settings.api_version
        )

        with APIClient(client_args) as client:

            # Try / Catch to get exceptions regarding
            # all checkpoint operations
            try:
                # Login to server:
                login_res = client.login(settings.sms_username, settings.sms_password)

                # If login is not successful, log the error message.
                if login_res.success is False:
                    raise Exception(Const.ERROR_CONNECTION_SMS_FAILED)
                else:
                    display(
                        Const.MESSAGE_CONNECTION_SMS_SUCCESSFUL.format(settings.sms_ip)
                    )

                    # Iterate through each row
                    # in the excel table
                    # Index is not used here but should
                    # NOT BE REMOVED
                    for index, row in dataframe.iterrows():

                        # Create a User object
                        # Filter data in excel
                        # data filtered are user email, groups assigned and
                        # action need to be taken
                        user = User(
                            row["User Email"],
                            str(row["Groups"]).split(";"),
                            row["Action"],
                        )

                        # This is the main function which
                        # handles all the logic
                        # Checks the action and determines
                        # which functions to call
                        action_checker(client, user)

                    # If everything worked
                    # publish the session to the SMS
                    publish(client)

                    # Install the policy
                    install_policy(client, settings)

            except Exception as e:
                # Prints the error message
                # and starts discarding the session
                display(Const.ERROR_INTERNAL.format(e))
                display(Const.MESSAGE_SESSION_DISCARDING)

                # Discard the active session
                discard(client)

                exit(1)

    except Exception as e:
        # Prints the error message
        display(Const.ERROR_INTERNAL.format(e))

        exit(1)


if __name__ == "__main__":
    main()
