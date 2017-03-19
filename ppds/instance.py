'''defines instances and logic'''
import os
import sys
import ppds.config
import ppds.hostfilepatch
PERMERROR = '''
Please run as your normal user so permission errors do not occur.
Use --root to override.
'''
VERSIONSTRING = """"
PPDS 0.0.1.dev0

Private Peer Domain Syndication: copyright 2017 by Andrew Donshik
Licensed under the GPL v3.0
THIS SOFTWARE IS PROVIDED AS-IS
WITHOUT WARRANTY OR LIABILITY AS THE LAW PERMITS
"""


def checkroot():
    '''checks UID and sets root flag'''
    return bool(os.getuid() == 0)


def checkaccess(location):
    '''validates access to a file'''
    if os.access(location, os.W_OK):
        return True
    else:
        return 'rootneeded'


class Instance(object):
    ''' Manages execution (mode should be cli or gui)'''
    def __init__(self, args, mode):
        self.args = args
        self.mode = mode
        self.configuration = ppds.config.Configuration()
        self.isroot = checkroot()
        self.run()

    def main(self):  # pylint: disable=E0211, R0201
        '''main program logic--to be replaced with instance exec logic'''
        return 'empty instance'

    def run(self):
        '''execs instance logic'''
        self.main()


class Cli(Instance):
    ''' cli specific methods '''
    def __init__(self, args, mode):
        self.helpmessage = """
USAGE:
(in order of priority)
--version:    prints version string
--autoconfig: generates default configuration file
--add:        adds repository to config; checks status of repository
--forceadd:   adds repository to config without status check
--patch:      patches the hosts file of the computer (must be root)
--unpatch:    removes any patches created by ppds (must be root)
--help:       prints this message
"""
        Instance.__init__(self, args, mode)

    def version(self):
        ''' prints versionstring '''
        if self.mode == 'cli':
            print(VERSIONSTRING)

    def autoconfig(self):
        '''auto configures config.json with default values'''
        self.configuration.autoconfig()
        print("Creating config.json with default settings")
        if self.isroot:
            print("Overwriting as root.")
        self.configuration.save()
        sys.exit(0)

    def addrepo(self):
        """adds ppds repostiory and tests avaliablity"""
        newrepo = str(input("Repository to add: "))
        if newrepo in self.configuration.repositories:
            print('Repo already added.')
            sys.exit(1)
        if self.configuration.addrepo(newrepo) != "failure":
            if self.isroot:
                print("Overwriting as root.")
            else:
                self.configuration.save()
                print("Added.")
                sys.exit(0)
        else:
            print("Repository is down. Aborting.")
            sys.exit(1)

    def forceaddrepo(self):
        """adds ppds repository without testing availability"""
        print("""
Adding repository without testing validity:
Exceptions may occur.""")
        newrepo = str(input("Repository to add: "))
        if newrepo in self.configuration.repositories:
            print('Repo already added.')
            sys.exit(1)
        self.configuration.forceaddrepo(newrepo)
        if self.isroot:
            print("Overwriting as root.")
        print("Added.")
        self.configuration.save()
        sys.exit(0)

    def patch(self):
        """
patches hostsfiles with all enabled packages and backs up previous hosts"""
        if self.configuration.load() != "No File":
            if self.isroot is False:
                print("Please restart the program with root permissions.")
                sys.exit(1)
            else:
                self.configuration.initrepolist()
                for item in self.configuration.repoobjectdict:
                    self.configuration.repoobjectdict[item].loadpackagelist()
                    self.configuration.repoobjectdict[item].loadjson()
                patcher = ppds.hostfilepatch.HostPatch(self.configuration)
                patcher.createpatch()
                if patcher.patchhosts() != "exists":
                    print("Hostsfile patched sucessfully.")
                    self.configuration.unloadrepolist()
                    sys.exit(0)
                else:
                    print("Patcher has already been used on this hosts file.")
                    self.configuration.unloadrepolist()
                    sys.exit(1)

    def unpatch(self):
        '''unpatches the host file by restoring previously taken backup'''
        if self.isroot is False:
            print("Please restart the program with root permissions.")
            sys.exit(1)
        else:
            patcher = ppds.hostfilepatch.HostPatch(self.configuration)
            if patcher.unpatchhosts() != "nobackup":
                print('Successfully unpatched hosts.')
                sys.exit(0)
            else:
                print("No hostsfile backup.")
                sys.exit(1)

    def printhelp(self):
        ''' prints help message'''
        print(self.helpmessage)

    def main(self):
        if (self.configuration.load() == "No File" and
                "--autoconfig" not in self.args and
                "--version" not in self.args):
            print("Please generate a config.json with --autoconfig.")
        if "--version" in self.args:
            self.version()
        elif "--autoconfig" in self.args:
            self.autoconfig()
        elif "--add" in self.args:
            self.addrepo()
        elif "--forceadd" in self.args:
            self.forceaddrepo()
        elif "--patch" in self.args:
            self.patch()
        elif "--unpatch" in self.args:
            self.unpatch()
        else:
            self.printhelp()
