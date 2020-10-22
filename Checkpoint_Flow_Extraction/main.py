from cpapi import APIClient, APIClientArgs
from settings import Settings
import constants as Const

######################################
############ My Functions ############
######################################

# Displays a message
def display(message):
    # TODO("Use a logger instead")
    print(message)


# Discard the session from the SMS
def discard(client):
    response = client.api_call("discard", {})
    response_logger(response, Const.MESSAGE_SESSION_DISCARDED)


# Checks if the response is
# successful or not
def response_logger(response, successMessage):
    if response.success:
        if successMessage is not None:
            display(successMessage)
        return True
    else:
        raise Exception(response.error_message)


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
