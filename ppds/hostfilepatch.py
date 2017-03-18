'''object to patch the hostfile and resolve conficts'''
import os
import shutil


class HostPatch:
    '''functions for patching ppds to the host file'''
    def __init__(self, configuration):
        '''copy relevant vars from configuration'''
        self.location = configuration.patchlocation
        self.hostlocation = configuration.hostfile  # may error on windows
        self.repoobjectdict = configuration.repoobjectdict
        self.hostentries = []
        self.ipentries = []

    def createpatch(self):
        '''generates file to append to hosts'''
        if os.path.isfile(self.location):
            os.remove(self.location)
        filevar = (open((self.location), 'a+'))
        filevar.write('##PATCHED BY PPDS## \n')
        self.hostentries = []
        self.ipentries = []
        for repo in self.repoobjectdict:
            for package in self.repoobjectdict[repo].hosts:
                for entry in self.repoobjectdict[repo].hosts[package]:
                    if entry not in self.hostentries:
                        if (self.repoobjectdict[repo].hosts[package][entry]
                                not in self.ipentries):
                            self.ipentries.append(
                                self.repoobjectdict[repo].hosts[package][entry]
                            )
                            self.hostentries.append(entry)
                            filevar.write(
                                self.repoobjectdict[repo].hosts[package][entry]
                                + ' ' + entry + '\n')
        filevar.close()

    def patchhosts(self):
        ''' patches host file '''
        if os.access(self.hostlocation, os.W_OK):
            with open(('%s/hosts' % self.hostlocation), 'r') as filevar:
                if '##PATCHED BY PPDS##' in filevar.read():
                    return 'exists'
            shutil.copy((('%s/hosts') % self.hostlocation),
                        ('%s/hosts.bak' % self.hostlocation))
            filein = open(('%s/hosts' % self.hostlocation), 'r')
            fileone = filein.read()
            filein.close()
            filein = open(self.location, 'r')
            filetwo = filein.read()
            filein.close()
            dataout = '\n' + fileone + filetwo
            fileout = open((('%s/hosts') % self.hostlocation), 'w')
            fileout.write(dataout)
        else:
            return 'rootneeded'

    def unpatchhosts(self):
        ''' unpatches host file'''
        if os.access(self.hostlocation, os.W_OK):
            if os.path.isfile('%s/hosts.bak' % self.hostlocation):
                os.remove('%s/hosts' % self.hostlocation)
                shutil.move((('%s/hosts.bak') % self.hostlocation),
                            ('%s/hosts' % self.hostlocation))
            else:
                return 'nobackup'
        else:
            return 'rootneeded'
