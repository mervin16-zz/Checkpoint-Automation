from cpapi import APIClient, APIClientArgs
import json


def publish(client):
    response = client.api_call(
        "publish", {})

    if response.success == False:
        print('An error occurred while publishing')
        exit(1)
    else:
        print("Session published successfully.")


def generic_group_uid(client):
    response = client.api_call(
        "show-generic-objects", {"name": "MyTestUserGroup"})

    if response.success == False:
        print(response)
        exit(1)
    else:
        jsondata = json.loads(json.dumps(response.data))

        for i in range(len(jsondata["objects"])):
            obj = jsondata["objects"][i]
            return obj["uid"]


def generic_user_uid(client):
    response_user = client.api_call(
        "add-generic-object", {"name": "genericuser12",
                               "create": "com.checkpoint.objects.classes.dummy.CpmiUser",
                               "authMethod": "INTERNAL_PASSWORD",
                               "internalPassword": "testpassword", })

    if response_user.success == False:
        print(response_user)
        exit(1)
    else:
        jsondata = json.loads(json.dumps(response_user.data))
        return jsondata["uid"]


def set_user_to_group(client, uuid, guid):
    response = client.api_call(
        "set-generic-object", {"uid": guid, "emptyFieldName": {"add": uuid}})

    if response.success == False:
        print(response)
        exit(1)
    else:
        print("success")


def main():
    ########################
    # Credentials
    sms_ip = "172.17.168.101"
    sms_username = "test1"
    sms_password = "1234"

    # initialize SMS session
    client_args = APIClientArgs(server=sms_ip, api_version=1.1)

    with APIClient(client_args) as client:
        # login to server:
        login_res = client.login(sms_username, sms_password)
        if login_res.success is False:
            print(
                "Login failed. Please check SMS version (this script works only with R80.xx)")
            exit(1)
        else:
            print('login success to: %s', sms_ip)

            guid = generic_group_uid(client)
            uuid = generic_user_uid(client)

            set_user_to_group(client, uuid, guid)

            publish(client)


if __name__ == '__main__':
    main()
