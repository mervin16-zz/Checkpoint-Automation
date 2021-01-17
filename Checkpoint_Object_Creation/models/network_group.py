from models.cobject import Object

# DO NOT instantiate this class directly
# Call the getInstance() or getInstanceVerification() method
# The getInstance() methods retrieve the data directly from the dict
# The getInstanceVerification() checks first if returned objects is not empty before retrieving data
# getInstanceVerification() is called when retrieving a list of Network Groups
# getInstance() is used after creation of Network Groups
class NGroup(Object):

    # Constructor
    def __init__(self, uid, name):
        # Instantiate parent class
        Object.__init__(self, uid, name)

    @staticmethod
    def getInstanceVerification(response):
        # Checks if response returned atleast an object
        # If atleast one object is present, it means
        # the object already exists with given IP address
        if response.data["total"] > 0:
            # Retrieve data from dict
            uid = response.data["objects"][0]["uid"]
            name = response.data["objects"][0]["name"]
            return NGroup(uid=uid, name=name)
        else:
            return None

    @staticmethod
    def getInstance(response):
        # Retrieve data from dict
        uid = response.data["uid"]
        name = response.data["name"]
        return NGroup(uid=uid, name=name)
