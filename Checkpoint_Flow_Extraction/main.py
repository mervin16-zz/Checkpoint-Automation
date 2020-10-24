from cpapi import APIClient, APIClientArgs
import pandas as pd
from settings import Settings
from flow import Rule, AccessRule, RuleIntermediator as RI
import constants as Const

######################################
############ My Functions ############
######################################

# Displays a message
def display(message):
    # TODO("Use a logger instead")
    print(message)


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

    response_checker(
        response,
        "Extracting flows for object {}".format(object_name),
        "The object {} doesn't exist. Skipping ...".format(object_name),
    )

    if not response.data["used-directly"]["access-control-rules"]:
        display("{} is not used anywhere".format(object_name))
        return None
    else:
        # Filter and order list
        filtered_list = RI.order_by_package_name(
            RI.filter_layer_type(response.data["used-directly"]["access-control-rules"])
        )

        # Check if list is not empty before proceeding
        if not filtered_list:
            return None

        return RI.fetch_rules(object_name, filtered_list)


def fetch_access_rules(client, rules):
    for rule in rules:
        pass
    pass


#####################################
########### Main Function ###########
#####################################
def main():
    # Try / Catch to get exceptions regarding
    # excel file connections and
    # checkpoint api client initialization
    try:

        # Get settings from Settings class
        settings = Settings()

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
            # Try / Catch to get exceptions regarding
            # all checkpoint operations
            try:
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

                    # Iterate through each row
                    # in the excel table
                    # Index is not used here but should
                    # NOT BE REMOVED
                    for index, row in dataframe.iterrows():

                        object_name = row["Object Name"]

                        # Make an API call to fetch
                        # basic rule details where the object
                        # is being used
                        rules = fetch_basic_rule(client, object_name)

                        # Make multiple API calls for each access rules in each
                        # policy returned
                        access_rules = fetch_access_rules(client, rules)

            except Exception as e:
                # Prints the error message
                # and starts discarding the session
                display(Const.ERROR_INTERNAL.format(e))

                exit(1)

    except Exception as e:
        # Prints the error message
        display(Const.ERROR_INTERNAL.format(e))

        exit(1)


if __name__ == "__main__":
    main()
