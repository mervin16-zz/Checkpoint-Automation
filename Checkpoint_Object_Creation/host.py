# DO NOT instantiate this class directly
# Call the getInstance() method
# The getInstance() methods performs prelminary checks
# before returning a host object
class Host:
    def __init__(self, response):
        self.uid = response["uid"]
        self.name = response["name"]
        self.ip = response["ipv4-address"]

    @staticmethod
    def getInstance(response):
        # Checks if response returned atleast an object
        # If atleast one object is present, it means
        # the object already exists with given IP address
        if response.data["total"] > 0:
            return Host(response.data["objects"][0])
        else:
            return None
