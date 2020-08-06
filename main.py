from cpapi import APIClient, APIClientArgs
import json

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
        exit(1)


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


# Retrieve desired group and
# returns the group uid
def get_group(client, groupName):
    response = client.api_call("show-generic-objects", {"name": groupName},)

    isSuccess = response_logger(response, "searching for group...")

    if isSuccess:
        jsondata = json.loads(json.dumps(response.data))

        if len(jsondata["objects"]) == 0:
            raise Exception(
                "There are no user gorups with the name {}".format(groupName)
            )
        else:
            for i in range(len(jsondata["objects"])):
                obj = jsondata["objects"][i]
                return obj["uid"]


# Assigns user to group
def assign_user_to_group(client, uuid, guid):
    response = client.api_call(
        "set-generic-object", {"uid": guid, "emptyFieldName": {"add": uuid}}
    )
    response_logger(response, "User has been added to group")


def main():
    # SMS Credentials
    sms_ip = "172.17.168.101"
    sms_username = "test1"
    sms_password = "1234"

    try:
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

                # Creates the user and return the UID
                uuid = create_user(client, "Mervin Hemaraju", "12345")
                # Fetches the group UID
                guid = get_group(client, "MyTestUserGroup")
                # Assign user to group
                assign_user_to_group(client, uuid, guid)
                # Publish the session
                publish(client)
    except Exception as e:
        print("An internal error occurred. Error: {}".format(e))
        exit(1)


if __name__ == "__main__":
    main()
