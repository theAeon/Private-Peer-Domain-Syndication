import json, os

class hostpatch():
    def __init__(self, configuration):
        self.location = configuration.patchlocation
        self.repositories = configuration.repositories
        self.jsonlist = []
    def loadjson(self):
        for repository in self.repositories:
            for filename in os.listdir('repos/%s' % repository):
                with open ('repos/%s/%s' % (repository, filename), 'r+', ) as f:
                    if filename != ".DS_Store":
                        self.jsonlist.append('%s' % filename)
                        print ('repos/%s/%s' % (repository, filename))
                        filename = json.load(f)
                        print(filename)
                        print(self.jsonlist)
