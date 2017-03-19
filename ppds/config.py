'''contains configuration class- applies and stores configuration'''
import sys
import json
import os
import shutil
import requests
import ppds.repository


def testrepo(repo):
    '''send http request to repolist on host'''
    try:
        repourl = 'http://' + repo
        request = requests.get("%s/ppdslist.json" % repourl,
                               allow_redirects=False)
        request.raise_for_status()
    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.MissingSchema):
        try:
            repourl = 'https://' + repo
            request = requests.get("%s/ppdslist.json" % repourl,
                                   allow_redirects=False)
            request.raise_for_status()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.MissingSchema):
            return 'down'


class Configuration:
    # pylint: disable=too-many-instance-attributes
    '''everything to do with configuration in a convenient class'''
    def __init__(self):
        '''define all aspects of configuration'''
        self.repositories = []
        self.platform = ''
        self.hostfile = ''
        self.patchlocation = 'hosts.patch'
        self.defaultdomain = 'repo.ppds.me'
        self.repoobjectdict = {}
        self.repopriority = {}
        self.__dict__ = self.__dict__

    def printdict(self):
        '''debug'''
        print(self.__dict__)

    def autoconfig(self):
        '''detect platform and hosts file location (windows may be wrong
        append default repo (repo.ppds.me)(pls no stealerino my domainerino)'''
        self.platform = sys.platform
        if self.platform == 'darwin' or 'linux':
            self.hostfile = '/etc/'
        elif self.platform == 'win32':
            return 'windows not yet supported'
            # self.hostfile = '%\SystemRoot%\\System32\\drivers\\etc\\'
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
        cfg = open('config.json', 'w+')
        json.dump(self.__dict__, cfg)
        cfg.close()
        return 'created'

    def load(self):
        '''load config from config.json'''
        if os.path.isfile('config.json'):
            cfg = open('config.json', 'r+')
            self.__dict__ = json.load(cfg)
            cfg.close()
        else:
            return 'No File'

    def makerepofolders(self):
        '''make folders for all repos in the repository list'''
        if not os.path.exists('repos'):
            os.mkdir('repos')
        for entry in self.repositories:
            if not os.path.exists('repos/%s/' % entry):
                os.makedirs('repos/%s/' % entry)

    def addrepo(self, repo):
        '''add repo to list, checking for server status'''
        if testrepo(repo) == 'down':
            return "failure"
        self.repositories.append(repo)
        self.makerepofolders()

    def forceaddrepo(self, repo):
        '''add repo to list regardless of server status'''
        self.repositories.append(repo)
        self.makerepofolders()

    def removerepo(self, repo):
        '''removes repo from list'''
        if repo in self.repositories:
            self.repositories.remove(repo)
            shutil.rmtree('repos/%s/' % repo)
        else:
            return 'repo does not exist'

    def initrepolist(self):
        '''adds repository class to list
        unload before saving or modifying please'''
        self.definerepopriority()
        for item in self.repositories:
            self.repoobjectdict[item] = ppds.repository.Repository(item,
                                                                   self)

    def unloadrepolist(self):
        '''clears repository classes'''
        self.repoobjectdict = {}

    def definerepopriority(self):
        ''' assigns each repo a number based on order in list '''
        self.repopriority = dict((name, order) for order, name in
                                 enumerate(self.repositories))
