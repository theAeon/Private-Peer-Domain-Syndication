import json, os, shutil

class HostPatch:
    def __init__(self, configuration):
        #copy relevant vars from configuration
        self.location = configuration.patchlocation
        self.hostlocation = configuration.hostfile ##may error on windows
        self.repoobjectdict = configuration.repoobjectdict
        self.hostentries = []
        self.ipentries = []
    def createpatch(self):
        if os.path.isfile(self.location):
            os.remove(self.location)
        f = (open((self.location), 'a+'))
        f.write('##PATCHED BY PPDS## \n')
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
    def patchhosts(self):
        if os.access(self.hostlocation, os.W_OK) == True:
            with open(('%s/hosts' % self.hostlocation), 'r') as f:
                if '##PATCHED BY PPDS##' in f.read():
                    return 'exists'
            shutil.copy((('%s/hosts') % self.hostlocation), ('%s/hosts.bak' % self.hostlocation))
            filein = open(('%s/hosts' % self.hostlocation), 'r')
            fileone = filein.read()
            filein.close()
            filein = open(self.location, 'r')
            filetwo = filein.read()
            filein.close()
            dataout = '\n' + fileone + filetwo
            fileout = open((('%s/hosts') % self.hostlocation), 'w')
            fileout.write(dataout)
            fileout.close
        else:
            return 'rootneeded'

    def unpatchhosts(self):
        if os.access(self.hostlocation, os.W_OK) == True:
            if os.path.isfile('%s/hosts.bak' % self.hostlocation) == True:
                os.remove('%s/hosts' % self.hostlocation)
                shutil.copy((('%s/hosts.bak') % self.hostlocation), ('%s/hosts' % self.hostlocation))
            else:
                return 'nobackup'
        else:
            return 'rootneeded'
