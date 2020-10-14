from cpapi import APIClient, APIClientArgs
import json
from host import Host
from network import Network
from settings import Settings
import constants as Const

# TODO("Remove when done with project")
from pprint import pprint
import traceback


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


def create_host(client, host_name, host_ip):

    # Checks if the host is already present
    is_host_present = check_host_existance(client, host_name, host_ip)

    # If host is not present
    # Create the host
    if is_host_present:
        display("Host already present")
    else:
        response = client.api_call(
            "add-host", {"name": host_name, "ip-address": host_ip}
        )
        response_logger(response, "{} has been created".format(host_name))


def check_host_existance(client, host_name, host_ip):

    # Make the API call to get all objects of type 'host'
    # matching the ip address
    response = client.api_call(
        "show-objects", {"in": ["text", host_ip], "type": "host"}
    )

    # Checks if request is successfull
    if response_logger(response, "Processing the object {}".format(host_name)):

        # Get the response and convert to Host object
        host = Host.getInstance(response)

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
    else:
        raise Exception("An error occured while processing object")


def create_network(client, network_name, network_subnet, subnet_mask):

    # Checks if the network is already present
    is_network_present = check_network_existance(client, network_name, network_subnet)

    # If network is not present
    # Create the network
    if is_network_present:
        display("Network already present")
    else:
        print(subnet_mask)
        response = client.api_call(
            "add-network",
            {
                "name": network_name,
                "subnet": network_subnet,
                "subnet-mask": subnet_mask,
            },
        )
        response_logger(response, "{} has been created".format(network_name))


def check_network_existance(client, network_name, network_subnet):

    # Make the API call to get all objects of type 'network'
    # matching the ip address
    response = client.api_call(
        "show-objects", {"in": ["text", network_subnet], "type": "network"}
    )

    # Checks if request is successfull
    if response_logger(response, "Processing the object {}".format(network_name)):

        # Get the response and convert to Network object
        network = Network.getInstance(response)

        if network is None:
            # We return false stating that the
            # network doesn't exist and that
            # we need to create one
            return False
        else:
            # We check if the IP address matches
            # If it matches, the network already exists
            # We therefore do not need to create another one, therefore returning true
            # Else, we return false stating that the network doesn't already exist
            if network.subnet == network_subnet:
                return True
            else:
                return False
    else:
        raise Exception("An error occured while processing object")


# Logic to create the object in Checkpoint
def create_object(client, object_name, object_ip):

    # Checks if object is a
    # host or a network
    if "/" in object_ip:
        # Means that this is a network
        # Split the subnet and subnet mask
        subnet_info = str(object_ip).split("/")
        # Get the subnet
        subnet = subnet_info[0].strip()
        # Get the subnet mask
        subnet_mask = subnet_info[1].strip()

        # Create the network
        create_network(client, object_name, subnet, Const.subnet_mapper[subnet_mask])
    else:
        # Means that this is a host
        create_host(client, object_name, object_ip)


###########################################
############## Main Function ##############
###########################################

# This is the main function where we instantiate
# the checkpoint api client
def main():

    # Get settings from Settings class
    settings = Settings()

    # Initialize the SMS session
    client_args = APIClientArgs(
        server=settings.sms_ip, api_version=settings.api_version
    )

    with APIClient(client_args) as client:

        # Catch any errors/exceptions and logs it
        try:
            # Login to SMS:
            login_res = client.login(settings.sms_username, settings.sms_password)

            # If login is not successful, raise an error message.
            if login_res.success is False:
                raise Exception(
                    "Login failed. Please check SMS version (this script works only with R80.xx)"
                )
            else:
                # Displays a message that we
                # successfully connected to the sms
                display("Successfully connected to: {}".format(settings.sms_ip))

                # FIXME("TEMPORARY INFO")
                host_name = "Net_172.0.0.0_9"
                host_ip = "172.0.0.0/9"

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

            # TODO("Remove when done with project")
            traceback.print_exc()

            exit(1)


if __name__ == "__main__":
    main()
