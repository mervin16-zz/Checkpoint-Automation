# DO NOT instantiate this class directly
# Call the getInstance() method
# The getInstance() methods performs prelminary checks
# before returning a host object
class Host:
    def __init__(self, response):
        self.uid = response.data["uid"]
        self.name = response.data["name"]
        self.ip = response.data["ipv4-address"]

    @staticmethod
    def getInstance(response):
        if response.success:
            return Host(response)
        else:
            return None
