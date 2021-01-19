from cpapi import APIClient, APIClientArgs
import pandas as pd
from datetime import datetime
import os
from utils.settings import Settings
from models.flow import AccessRule, RuleIntermediator as RI
import utils.constants as Const
from utils.utils import create_logger

# TODO("Improve object searching")
# TODO("Fix bug when comment is empty")

######################################
########## Global Variables ##########
######################################
logger = None
settings = Settings()


######################################
############ My Functions ############
######################################

# Displays a message
def display(message):
    logger.info(message)


# Checks if the response is
# successful or not
def response_checker(response, successMessage, errorMessage):
    # Checks if request was successfull
    if response.success:
        # If successful, checks whether to display message or not
        if successMessage is not None:
            display(successMessage)
        return True
    # If request was not successfull
    elif not response.success:
        # Checks if response code is 'object not found'
        if response.data["code"] == "generic_err_object_not_found":
            if errorMessage is not None:
                display(errorMessage)
            return False

    raise Exception(response.error_message)


def fetch_basic_rule(client, object_name):
    response = client.api_call("where-used", {"name": object_name})

    is_success = response_checker(
        response,
        Const.MESSAGE_EXTRACTING_FLOWS_FOR_OBJECT.format(object_name),
        Const.MESSAGE_OBJECT_DOESNT_EXIST.format(object_name),
    )

    if is_success:
        if not response.data["used-directly"]["access-control-rules"]:
            display(Const.MESSAGE_OBJECT_NOT_USED.format(object_name))
            return None
        else:
            # Filter and order list
            filtered_list = RI.order_by_package_name(
                RI.filter_layer_type(
                    response.data["used-directly"]["access-control-rules"]
                )
            )

            # Check if list is not empty before proceeding
            if not filtered_list:
                display(Const.MESSAGE_OBJECT_NOT_USED.format(object_name))
                return None

            return RI.fetch_rules(filtered_list)
    else:
        return None


def fetch_access_rules(client, policy_rules_dict, queried_object):

    access_rules = []

    # For each policy in the dict
    for policy in policy_rules_dict:

        # For each uids in the policy
        for uid in policy_rules_dict[policy]["uids"]:

            response = client.api_call(
                "show-access-rule", {"uid": uid["id"], "layer": uid["layer-name"]},
            )

            is_success = response_checker(
                response, None, Const.ERROR_FLOW_FETCHING.format(uid, policy),
            )

            if is_success:
                access_rules.append(
                    AccessRule.getInstance(response.data, policy, queried_object)
                )
            else:
                return None

    return access_rules


def export_rules(access_rules):

    rows = []

    # Export all into rows
    for ar in access_rules:

        row = [
            ar.queried_object,
            ar.name,
            ar.policy,
            ar.source,
            ar.destination,
            ar.service,
            ar.action,
            ar.comment,
        ]

        rows.append(row)

    # Creates a data frame for exporting to excel
    dataframe = pd.DataFrame(
        rows,
        columns=[
            "Queried Object",
            "Rule Name",
            "Policy",
            "Source(s)",
            "Destination(s)",
            "Service(s)",
            "Action",
            "Comments",
        ],
    )

    # Write to excel file
    dataframe.to_excel(settings.output_data_path)

    # Generate message for user
    display(Const.MESSAGE_EXTRACTION_COMPLETE.format(settings.output_data_path))


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

        # Read data from file
        dataframe = pd.read_excel(settings.object_data_path)
        # Since blank cells return 'nan' instead of empty string
        # we replace all 'nan' with an empty string
        dataframe = dataframe.fillna("")

        # Initialize the SMS session
        client_args = APIClientArgs(
            server=settings.sms_ip, api_version=settings.api_version
        )

        with APIClient(client_args) as client:

            # Login to SMS:
            login_res = client.login(settings.sms_username, settings.sms_password)

            # If login is not successful, raise an error message.
            if login_res.success is False:
                raise Exception(Const.ERROR_LOGIN_FALED)
            else:
                # Displays a message that we
                # successfully connected to the sms
                display(
                    Const.MESSAGE_CONNECTION_SMS_SUCCESSFULL.format(settings.sms_ip)
                )

                access_rules = []

                # Iterate through each row
                # in the excel table
                # Index is not used here but should
                # NOT BE REMOVED
                for index, row in dataframe.iterrows():

                    object_name = row["Object Name"]

                    # Make an API call to fetch
                    # basic rule details where the object
                    # is being used
                    policy_rules_dict = fetch_basic_rule(client, object_name)

                    if policy_rules_dict != None:
                        # Make multiple API calls for each access rules in each
                        # policy returned
                        a_rules = fetch_access_rules(
                            client, policy_rules_dict, object_name
                        )

                        if a_rules != None:
                            # Extend the list
                            access_rules.extend(a_rules)

                if access_rules != None:
                    # Export access rules
                    export_rules(access_rules)

    except Exception as e:
        # Prints the error message
        display(Const.ERROR_INTERNAL.format(e))

        exit(1)


if __name__ == "__main__":
    main()
