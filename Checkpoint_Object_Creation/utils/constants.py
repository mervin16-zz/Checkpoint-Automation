###################################
############ Constants ############
###################################

# CIDR to subnet mask mapping
subnet_mapper = {
    "1": "128.0.0.0",
    "2": "192.0.0.0",
    "3": "224.0.0.0",
    "4": "240.0.0.0",
    "5": "248.0.0.0",
    "6": "252.0.0.0",
    "7": "254.0.0.0",
    "8": "255.0.0.0",
    "9": "255.128.0.0",
    "10": "255.192.0.0",
    "11": "255.224.0.0",
    "12": "255.240.0.0",
    "13": "255.248.0.0",
    "14": "255.252.0.0",
    "15": "255.254.0.0",
    "16": "255.255.0.0",
    "17": "255.255.128.0",
    "18": "255.255.192.0",
    "19": "255.255.224.0",
    "20": "255.255.240.0",
    "21": "255.255.248.0",
    "22": "255.255.252.0",
    "23": "255.255.254.0",
    "24": "255.255.255.0",
    "25": "255.255.255.128",
    "26": "255.255.255.192",
    "27": "255.255.255.224",
    "28": "255.255.255.240",
    "29": "255.255.255.248",
    "30": "255.255.255.252",
    "31": "255.255.255.254",
    "32": "255.255.255.255",
}


# Messages
MESSAGE_SESSION_DISCARDING = "Discarding the session..."
MESSAGE_SESSION_DISCARDED = "Session has been discarded."
MESSAGE_SESSION_PUBLISHED = "Session published successfully."
MESSAGE_CONNECTION_SMS_SUCCESSFULL = "Successfully connected to: {}"
MESSAGE_OBJECT_ASSIGNED_TO_GROUP = "Object {} has been assigned to group {}"
MESSAGE_GROUP_CREATION_AND_ASSIGNMENT = "Creating the group {} and adding member {}"
MESSAGE_GROUP_PROCESSING = "Processing the group {}"
MESSAGE_OBJECT_PROCESSING = "Processing the object {}"
MESSAGE_NETWORK_ALREADY_PRESENT = "Network already present under name {}"
MESSAGE_HOST_ALREADY_PRESENT = "Host already present under name {}"
MESSAGE_OBJECT_CREATED = "{} has been created"

# Error Messages
ERROR_INTERNAL = "An internal error occurred. Error: {}"
ERROR_LOGIN_FALED = (
    "Login failed. Please check SMS version (this script works only with R80.xx)"
)
ERROR_HOST_NAME_IP_MISMATCH = "A host object exists with the same name but different IP. Please check before running script."
