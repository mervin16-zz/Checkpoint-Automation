# This is the parent class of all objects in Checkpoint
# 'uid' and 'name' is common for all objects
# Currently, Network and Host objects are direct child of Object
class Object:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
