'''defines instances and logic'''
import os
import ctypes
import sys
import shutil
import ppds.config
import ppds.hostfilepatch
PERMERROR = '''
Please run as your normal user so permission errors do not occur.
Use --root to override.
'''
VERSIONSTRING = """
PPDS 0.0.1.dev2

Private Peer Domain Syndication: copyright 2017 by Andrew Donshik
Licensed under the GPL v3.0
THIS SOFTWARE IS PROVIDED AS-IS
WITHOUT WARRANTY OR LIABILITY AS THE LAW PERMITS
"""


def checkroot():
    '''checks UID and sets root flag on linux/osx'''
    return bool(os.getuid() == 0)

def checkadmin():
    '''checks admin on windows'''
    return bool(ctypes.windll.shell32.IsUserAnAdmin())


def checkaccess(location):
    '''validates access to a file'''
    if os.access(location, os.W_OK):
        return True
    return 'rootneeded'


class Instance(object):
    ''' Manages execution (mode should be cli or gui)'''
    def __init__(self, args, mode):
        self.args = args
        self.platform = sys.platform
        self.mode = mode
        if self.platform == 'darwin' or self.platform == 'linux':
            self.isroot = checkroot()
        elif self.platform == 'win32':
            self.isroot = checkadmin()

        self.configuration = ppds.config.Configuration(self.mode,
                                                       self.isroot, self.args)
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
--add:        adds repository to config; checks status of repository
--forceadd:   adds repository to config without status check
--patch:      patches the hosts file of the computer (must be root)
--unpatch:    removes any patches created by ppds (must be root)
--list        lists all repositories and packages
--remove      remove a repository from config
--help:       prints this message
"""
        Instance.__init__(self, args, mode)

    def version(self):
        ''' prints versionstring '''
        if self.mode == 'cli':
            print(VERSIONSTRING)

    def addrepo(self):
        """adds ppds repostiory and tests avaliablity"""
        newrepo = str(input("Repository to add: "))
        if newrepo in self.configuration.repositories:
            print('Repo already added.')
            sys.exit(1)
        if self.configuration.addrepo(newrepo,
                                      self.isroot, self.args) != "failure":
            if self.isroot:
                print("Overwriting as root.")
            else:
                self.configuration.save(self.mode, self.isroot, self.args)
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
        self.configuration.forceaddrepo(newrepo, self.isroot, self.args)
        if self.isroot:
            print("Overwriting as root.")
        print("Added.")
        self.configuration.save(self.mode, self.isroot, self.args)
        sys.exit(0)

    def patch(self):
        """
patches hostsfiles with all enabled packages and backs up previous hosts

REQUIRES ppdslist.json in repofolders or WILL CRASH (a dictionary of all json
files with value enable/disable)
"""
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
    def listrepo(self):
        ''' lists all repos with enabled packages '''
        self.configuration.initrepolist()
        for item in self.configuration.repoobjectdict:
            print('\n')
            print(item)
            self.configuration.repoobjectdict[item].loadpackagelist()
            for package in self.configuration.repoobjectdict[item].packages:
                print('- ' + package + ' -- ' + self.configuration.repoobjectdict[item].packages[package])
        self.configuration.unloadrepolist()
    def removerepo(self):
        '''remove a repo and it's respective folders'''
        repo = str(input('Repository to remove: '))
        self.configuration.repositories.remove(repo)
        shutil.rmtree(self.configuration.datafolder + '/repos/' + repo)
        self.configuration.save(self.mode, self.isroot, self.args)
    def printhelp(self):
        ''' prints help message'''
        print(self.helpmessage)

    def main(self):
        if "--version" in self.args:
            self.version()
        elif "--add" in self.args:
            self.addrepo()
        elif "--forceadd" in self.args:
            self.forceaddrepo()
        elif "--patch" in self.args:
            self.patch()
        elif "--unpatch" in self.args:
            self.unpatch()
        elif "--list" in self.args:
            self.listrepo()
        elif "--remove" in self.args:
            self.removerepo()
        else:
            self.printhelp()
