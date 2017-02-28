import json, os

class hostpatch():
    def __init__(self, configuration):
        self.location = configuration.patchlocation
        self.repositories = configuration.repositories
        self.jsondict = {}
    def loadjson(self):
        for repository in self.repositories:
            for filename in os.listdir('repos/%s' % repository):
                with open ('repos/%s/%s' % (repository, filename), 'r+', ) as f:
                    if filename != ".DS_Store":
                        print ('repos/%s/%s' % (repository, filename))
                        fileproduct = json.load(f)
                        self.jsondict['%s/%s' % (repository, filename)] = fileproduct
                        print(fileproduct)
                        print(self.jsondict)
