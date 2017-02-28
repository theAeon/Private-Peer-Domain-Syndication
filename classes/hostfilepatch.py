import json, os

class hostpatch():
    def __init__(self, configuration):
        #copy relevant vars from configuration
        self.location = configuration.patchlocation
        self.repoobjectdict = configuration.repoobjectdict
