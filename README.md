# Checkpoint Automation

This is a project for automating tasks in the Checkpoint Firewall Security version R80.XX.


# Installation

```pip install pandas```

```pip install --upgrade git+https://github.com/CheckPointSW/cp_mgmt_api_python_sdk```

# Tasks

Currently the project has the following tasks automated:

- User creation and assigning to groups
- Object creations

```More info soon ```

# Constraints

## User Mobility
- When providing the email of the user, the script takes everything before the ```@``` to create the name of the user. Hence, each user created will have distinct names.
- Available ```Actions``` are ```add```, ```edit``` and ```delete``` ONLY. Any other arguments provided in the action section will stop the script.
- If one row fails to process, the whole session is discarded and the error message will be provided to the user for he/she to fix it.
 - When adding a user, leaving the ```Groups``` section empty will result in the creation of the user ONLY.
- If you want to add the user to a group, you will need to specify the group name in the group section.
- If you want to add the user to multiple groups, you will need to separate the group name with a ```;```.
- The ```Action``` ```delete``` will remove the user completely whereas the action ```edit``` will remove users in specified groups.

## Object Creation
```Not Documented Yet ```
# File Formats
Still not standardized. Will be documented soon...

## User Mobility
We should always add user data in an excel with the following format:

![user_data_excel](Checkpoint_User_Mobility\screenshots\format_excel_user_data.png)

## Object Creation

```Not Documented Yet ```


# Settings

## User Mobility

All information about the SMS, API version and path of the user data excel sheet is ocnfigured in a ```config/settings.json file``` as such:

```
{
    "sms": {
        "host": "172.30.43.150",
        "username": "api",
        "password": "ptc686grt09",
        "gateways": ["CKP-GW-MU"],
        "policy": "Standard"
    },
    "api": {
        "version": 1.1
    },
    "user_data": {
        "path": "Checkpoint_User_Mobility/config/User-Mobility-Test.xlsx"
    }
}
```

Any changes to the sms credentials or path of the excel file should be changed in the settings file.


## Object Creation

```Not Documented Yet ```

# License
Copyright 2020 Mervin Hemaraju