###################################
############ Constants ############
###################################

# Information Messages
MESSAGE_CONNECTION_SMS_SUCCESSFUL = "Successfully connected to: {}"
MESSAGE_SESSION_DISCARDING = "Discarding the session..."
MESSAGE_SESSION_DISCARDED = "The session has been discarded"
MESSAGE_SESSION_PUBLISHED = "The session has been published successfully"
MESSAGE_POLICY_INSTALLING = "Installing policy..."
MESSAGE_POLICY_INSTALLED = "Policy has been installed"
MESSAGE_USER_REMOVED_FROM_GROUP = "User has been removed from group"
MESSAGE_USER_REMOVED = "The user {} has been deleted"
MESSAGE_USER_ADDED_TO_GROUP = "User has been added to group"
MESSAGE_GROUP_PROCESSING = "Processing the group {}"
MESSAGE_USER_PROCESSING = "Processing the user {}"
MESSAGE_USER_PASSWORD_GENERATED = "The password generated for the user is {}"

# Error Messages
ERROR_CONNECTION_SMS_FAILED = (
    "Login failed. Please check SMS version (this script works only with R80.xx)"
)
ERROR_INTERNAL = "An internal error occurred. Error: {}"

ERROR_ACTION_MISLEADING = "The action '{}' for user '{}' is misleading. Please enter the correct actions and try again."

ERROR_GROUP_FETCHING = "An error occured while getting the group {}"

ERROR_USER_FETCHING = "An error occured while getting the user {}"
