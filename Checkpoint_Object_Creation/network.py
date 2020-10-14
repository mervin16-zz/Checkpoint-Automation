# DO NOT instantiate this class directly
# Call the getInstance() method
# The getInstance() methods performs prelminary checks
# before returning a network object
class Network:
    def __init__(self, response):
        self.uid = response["uid"]
        self.name = response["name"]
        self.subnet = response["subnet4"]
        self.subnet_mask = response["subnet-mask"]

    @staticmethod
    def getInstance(response):
        # Checks if response returned atleast an object
        # If atleast one object is present, it means
        # the object already exists with given IP address
        if response.data["total"] > 0:
            return Network(response.data["objects"][0])
        else:
            return None
