import sys
import json
import os
import requests
import shutil
import classes.repository


# everything to do with configuration in a convenient class
class Configuration:
    def __init__(self):
        '''define all aspects of configuration'''
        self.repositories = []
        self.platform = ''
        self.hostfile = ''
        self.patchlocation = 'hosts.patch'
        self.defaultdomain = 'repo.ppds.me'
        self.repoobjectdict = {}
        self.repopriority = {}

    def printdict(self):
        # debug
        print(self.__dict__)

    def autoconfig(self):
        '''detect platform and hosts file location (windows may be wrong
        append default repo (repo.ppds.me)(pls no stealerino my domainerino)'''
        self.platform = sys.platform
        if self.platform == 'darwin' or 'linux':
            self.hostfile = '/etc/'
        elif self.platform == 'win32':
            self.hostfile = '%\SystemRoot%\\System32\\drivers\\etc\\'
        else:
            self.hostfile = str(input("Enter Plaintext Hostfile Location: "))
        self.repositories.append(self.defaultdomain)
        self.makerepofolders()

    def save(self):
        '''dump config to json'''
        if (any(self.repoobjectdict) is False and
           any(self.repopriority) is False):
            if os.path.isfile('config.json'):
                check = str(input('Overwrite config? (y/n): '))
                if check == 'y':
                    os.remove('config.json')
                else:
                    return 'cancelled'
        else:
            return 'notempty'
        f = open('config.json', 'w+')
        json.dump(self.__dict__, f)
        f.close()
        return('created')

    def load(self):
        '''load config from config.json'''
        if os.path.isfile('config.json'):
            f = open('config.json', 'r+')
            self.__dict__ = json.load(f)
            f.close()
        else:
            return ('No File')

    def makerepofolders(self):
        '''make folders for all repos in the repository list'''
        if not os.path.exists('repos'):
            os.mkdir('repos')
        for entry in self.repositories:
            if not os.path.exists('repos/%s/' % entry):
                os.makedirs('repos/%s/' % entry)

    def testrepo(self, repo):
        '''send http request to repolist on host'''
        try:
            repourl = 'http://' + repo
            r = requests.get("%s/ppdslist.json" % repourl,
                             allow_redirects=False)
            r.raise_for_status()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.MissingSchema):
            try:
                repourl = 'https://' + repo
                r = requests.get("%s/ppdslist.json" % repourl,
                                 allow_redirects=False)
                r.raise_for_status()
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError,
                    requests.exceptions.MissingSchema):
                return('down')

    def addrepo(self, repo):
        '''add repo to list, checking for server status'''
        if self.testrepo(repo) == 'down':
            return "failure"
        self.repositories.append(repo)
        self.makerepofolders()

    def forceaddrepo(self, repo):
        '''add repo to list regardless of server status'''
        self.repositories.append(repo)
        self.makerepofolders()

    def removerepo(self, repo):
        if repo in self.repositories:
            self.repositories.remove(repo)
            shutil.rmtree('repos/%s/' % repo)
        else:
            return 'repo does not exist'

    def initrepolist(self):
        '''adds repository class to list
        unload before saving or modifying please'''
        for item in self.repositories:
            self.repoobjectdict[item] = classes.repository.Repository(item,
                                                                      self)

    def unloadrepolist(self):
        '''clears repository classes'''
        self.repoobjectdict = {}

    def definerepopriority(self):
        self.repopriority = dict((name, order) for order, name in
                                 enumerate(self.repositories))
        print(self.repopriority)
