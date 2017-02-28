import json, os

class HostPatch:
    def __init__(self, configuration):
        #copy relevant vars from configuration
        self.location = configuration.patchlocation
        self.repoobjectdict = configuration.repoobjectdict
    def createpatch(self):
        if os.path.isfile(self.location):
            os.remove(self.location)
        for repo in self.repoobjectdict:
            for package in self.repoobjectdict[repo].hosts:
                for entry in self.repoobjectdict[repo].hosts[package]:
                    f = (open((self.location), 'a+'))
                    f.write(self.repoobjectdict[repo].hosts[package][entry] + ' ' + entry + '\n')
        f.close()
    def reolveconflict(self):
        return 'resolved'
