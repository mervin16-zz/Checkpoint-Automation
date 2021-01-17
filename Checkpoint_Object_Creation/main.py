from cpapi import APIClient, APIClientArgs
import pandas as pd
import os
from datetime import datetime
from models.host import Host
from models.network import Network
from utils.settings import Settings
from models.cobject import Object
from models.network_group import NGroup
import utils.constants as Const
from utils.utils import create_logger

######################################
########## Global Variables ##########
######################################
logger = None

##########################################
############## My Functions ##############
##########################################

# Publish the session to the SMS
def publish(client):
    response = client.api_call("publish", {})
    response_logger(response, Const.MESSAGE_SESSION_PUBLISHED)


# Discard the session from the SMS
def discard(client):
    response = client.api_call("discard", {})
    response_logger(response, Const.MESSAGE_SESSION_DISCARDED)


# Displays a message
def display(message):
    # Logs the message
    logger.info(message)


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
    host = check_host_existance(client, host_name, host_ip)

    if host is None:
        # Creates the host
        response = client.api_call(
            "add-host", {"name": host_name, "ip-address": host_ip}
        )

        response_logger(response, Const.MESSAGE_OBJECT_CREATED.format(host_name))

        # We then return the host object here
        return Host.getInstance(response)
    else:
        # We check if the IP address matches
        # If it matches, the host already exists
        # We therefore do not need to create another one, therefore returning true
        # Else, we return false stating that the host doesn't already exist
        if host.ip == host_ip:
            # Displays a message for user
            display(Const.MESSAGE_HOST_ALREADY_PRESENT.format(host.name))
            return host
        else:
            raise Exception(Const.ERROR_HOST_NAME_IP_MISMATCH)


def check_host_existance(client, host_name, host_ip):

    # Make the API call to get all objects of type 'host'
    # matching the ip address
    response = client.api_call(
        "show-objects", {"filter": host_ip, "ip-only": True, "type": "host"}
    )

    # Checks if request is successfull
    response_logger(response, Const.MESSAGE_OBJECT_PROCESSING.format(host_name))

    # Get the response and convert to Host object
    # Then return host object
    return Host.getInstanceVerification(response)


def create_network(client, network_name, network_subnet, subnet_mask):

    # Fetch all networks matching with subnet
    networks = fetch_networks(client, network_name, network_subnet)

    # Check if returned networks is not none
    if networks is not None:

        # Filter the list that matches matches subnet and subnet mask and
        # called next on the list
        # If no networks found, it will return None
        network = next(
            filter(
                lambda net: net.subnet == network_subnet
                and net.subnet_mask == subnet_mask,
                networks,
            ),
            None,
        )

        # We check if filtered network is None
        if network is not None:
            # Then the network already exists
            # Displays a message for the user
            display(Const.MESSAGE_NETWORK_ALREADY_PRESENT.format(network.name))
            # Return the network
            return network

    # If code reaches this line, it means
    # No networks were found in the filters
    # We then create the network
    response = client.api_call(
        "add-network",
        {"name": network_name, "subnet": network_subnet, "subnet-mask": subnet_mask,},
    )

    response_logger(response, Const.MESSAGE_OBJECT_CREATED.format(network_name))

    # We then return the new network object
    return Network.getInstance(response)


def fetch_networks(client, network_name, network_subnet):

    # Make the API call to get all objects of type 'network'
    # matching the ip address
    response = client.api_call(
        "show-objects", {"filter": network_subnet, "ip-only": True, "type": "network"}
    )

    # Checks if request was a success
    response_logger(response, Const.MESSAGE_OBJECT_PROCESSING.format(network_name))

    # Return network list
    return Network.getInstances(response)


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
        # and return a Network object
        network = create_network(
            client, object_name, subnet, Const.subnet_mapper[subnet_mask]
        )

        # Cast Network object to parent class Object
        network.__class__ = Object

        # Returns the parent class Object
        return network
    else:
        # Means that this is a host
        # and return a Host object
        host = create_host(client, object_name, object_ip)

        # Cast Host object to parent class Object
        host.__class__ = Object

        # Returns the parent class Object
        return host


def fetch_group(client, group, network_object):
    # Make the API call to get a list of groups matching the name
    response = client.api_call("show-objects", {"filter": group, "type": "group"})

    response_logger(response, Const.MESSAGE_GROUP_PROCESSING.format(group))

    return NGroup.getInstanceVerification(response)


def create_group_and_assign(client, group, network_object):
    # Make the API call to create the group and assign the object
    response = client.api_call(
        "add-group", {"name": group, "members": network_object.name}
    )

    # If request is a success
    # We just need to display a message
    response_logger(
        response,
        Const.MESSAGE_GROUP_CREATION_AND_ASSIGNMENT.format(group, network_object.name),
    )


def assign_to_group(client, group, network_object):
    # Make the API call to set object to the group
    response = client.api_call(
        "set-group", {"name": group.name, "members": {"add": network_object.name}}
    )

    # If request is a success
    # We just need to display a message
    response_logger(
        response,
        Const.MESSAGE_OBJECT_ASSIGNED_TO_GROUP.format(network_object.name, group.name),
    )


def object_assignment(client, network_object, groups):

    for group in groups:
        # get group name individually
        # removes all whitespaces as not allowed in checkpoint for network groups
        group = group.replace(" ", "")

        # Fetch the group details
        ngroup = fetch_group(client, group, network_object)

        # Check if groups is none
        # If it is none, it means no groups exists
        # under this name, we therefore need to create one
        # Else it means that the group already exists,
        # then we just need to assign it to the group
        if ngroup is None:
            # Create the group
            create_group_and_assign(client, group, network_object)
        else:
            # Assign the object to the group
            assign_to_group(client, ngroup, network_object)


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


###########################################
############## Main Function ##############
###########################################

# This is the main function where we instantiate
# the checkpoint api client
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
                        object_ip = row["Object IP"]
                        object_groups = str(row["Object Groups"]).split(";")

                        # Creates the object
                        # and returns an Object object
                        object_created = create_object(client, object_name, object_ip)

                        # Assign object to group
                        object_assignment(client, object_created, object_groups)

                    # Publish the session
                    publish(client)

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
