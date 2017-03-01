import json, os

class HostPatch:
    def __init__(self, configuration):
        #copy relevant vars from configuration
        self.location = configuration.patchlocation
        self.repoobjectdict = configuration.repoobjectdict
        self.hostentries = []
        self.ipentries = []
    def createpatch(self):
        if os.path.isfile(self.location):
            os.remove(self.location)
        f = (open((self.location), 'a+'))
        self.hostentries = []
        self.ipentries = []
        for repo in self.repoobjectdict:
            for package in self.repoobjectdict[repo].hosts:
                for entry in self.repoobjectdict[repo].hosts[package]:
                    if entry not in self.hostentries:
                        if self.repoobjectdict[repo].hosts[package][entry] not in self.ipentries:
                            self.ipentries.append(self.repoobjectdict[repo].hosts[package][entry])
                            self.hostentries.append(entry)
                            f.write(self.repoobjectdict[repo].hosts[package][entry]
                            + ' ' + entry + '\n')
        f.close()
