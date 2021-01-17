from models.cobject import Object

# DO NOT instantiate this class directly
# Call the getInstance() or getInstanceVerification() method
# The getInstance() method retrieve the data directly from the dict
# The getInstances() returns a list of matched subnets
# getInstances() is called when retrieving a list of Networks
# getInstance() is used after creation of Network
class Network(Object):

    # Constructor
    def __init__(self, uid, name, subnet, subnet_mask):
        # Instantiate parent class
        Object.__init__(self, uid, name)
        # Child vars
        self.subnet = subnet
        self.subnet_mask = subnet_mask

    @staticmethod
    def getInstances(response):
        # Checks if response has matches networks
        if response.data["total"] > 0:
            # If it mached some networks,
            # Create empty list of networks
            networks = []
            # Iterate through fetched networks
            for network in response.data["objects"]:
                # Retrieve data
                uid = network["uid"]
                name = network["name"]
                subnet = network["subnet4"]
                subnet_mask = network["subnet-mask"]
                # Add networks to list of networks
                networks.append(Network(uid, name, subnet, subnet_mask))
            # Return the list of networks
            return networks

        else:
            # No networks found
            return None

    @staticmethod
    def getInstance(response):
        # Retrieve data from dict
        uid = response.data["uid"]
        name = response.data["name"]
        subnet = response.data["subnet4"]
        subnet_mask = response.data["subnet-mask"]
        return Network(uid, name, subnet, subnet_mask)
