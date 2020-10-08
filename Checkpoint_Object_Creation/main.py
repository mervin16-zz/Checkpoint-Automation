from cpapi import APIClient, APIClientArgs
import json
from host import Host
from pprint import pprint

# Data that should be moved to a file
# SMS Credentials
sms_ip = "172.30.43.150"
sms_username = "api"
sms_password = "ptc686grt09"
api_version = 1.1


##########################################
############## My Functions ##############
##########################################

# Publish the session to the SMS
def publish(client):
    response = client.api_call("publish", {})
    response_logger(response, "Session published successfully.")


# Discard the session from the SMS
def discard(client):
    response = client.api_call("discard", {})
    response_logger(response, "Session has been discarded.")


# Displays a message
def display(message):
    # TODO("Use a logger instead of print")
    print(message)


# Checks if the response is
# successful or not
def response_logger(response, successMessage):
    if response.success:
        if successMessage is not None:
            display(successMessage)
        return True
    else:
        raise Exception(response.error_message)


# Creates a host in checkpoint
def create_host(client, host_name, host_ip):
    is_host_present = check_host_existance(client, host_name, host_ip)

    if is_host_present:
        display("Host already present")
    else:
        response = client.api_call(
            "add-host", {"name": host_name, "ip-address": host_ip}
        )
        response_logger(response, "{} has been created".format(host_name))


def check_host_existance(client, host_name, host_ip):
    # Get the response and convert to Host object
    host = Host.getInstance(client.api_call("show-host", {"name": host_name}))

    if host is None:
        # WE return false stating that the
        # host doesn't exist and that
        # we need to create one
        return False
    else:
        # We check if the IP address matches
        # If it matches, the host already exists
        # We therefore do not need to create another one, therefore returning true
        # Else, we return false stating that the host doesn't already exist
        if host.ip == host_ip:
            return True
        else:
            return False


# Logic to create the object in Checkpoint
def create_object(client, host_name, host_ip):
    create_host(client, host_name, host_ip)


###########################################
############## Main Function ##############
###########################################

# This is the main function where we instantiate
# the checkpoint api client
def main():

    # Initialize the SMS session
    client_args = APIClientArgs(server=sms_ip, api_version=api_version)

    with APIClient(client_args) as client:

        # Catch any errors/exceptions and logs it
        try:
            # Login to SMS:
            login_res = client.login(sms_username, sms_password)

            # If login is not successful, raise an error message.
            if login_res.success is False:
                raise Exception(
                    "Login failed. Please check SMS version (this script works only with R80.xx)"
                )
            else:
                # Displays a message that we
                # successfully connected to the sms
                display("Successfully connected to: {}".format(sms_ip))

                # FIXME("TEMPORARY INFO")
                host_name = "host_10.0.0.11"
                host_ip = "10.0.0.11"

                # Creates the object
                create_object(client, host_name, host_ip)

                # Publish the session
                publish(client)

        except Exception as e:
            # Prints the error message
            # and starts discarding the session
            display("An internal error occurred. Error: {}".format(e))
            display("Discarding the session...")

            # Discard the active session
            discard(client)

            exit(1)


if __name__ == "__main__":
    main()
