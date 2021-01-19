###################################
############ Constants ############
###################################

# Messages
MESSAGE_SESSION_DISCARDING = "Discarding the session..."
MESSAGE_SESSION_DISCARDED = "Session has been discarded."
MESSAGE_SESSION_PUBLISHED = "Session published successfully."
MESSAGE_CONNECTION_SMS_SUCCESSFULL = "Successfully connected to: {}"
MESSAGE_EXTRACTING_FLOWS_FOR_OBJECT = "Extracting flows for object {}"
MESSAGE_OBJECT_DOESNT_EXIST = "The object {} doesn't exist. Skipping ..."
MESSAGE_OBJECT_NOT_USED = "{} is not used anywhere"
MESSAGE_EXTRACTION_COMPLETE = "The flows have been extracted to the path '{}'"

# Error Messages
ERROR_INTERNAL = "An internal error occurred. Error: {}"
ERROR_LOGIN_FALED = (
    "Login failed. Please check SMS version (this script works only with R80.xx)"
)
ERROR_FLOW_FETCHING = "An error occured while fetching flow with uid {} in policy {}"
