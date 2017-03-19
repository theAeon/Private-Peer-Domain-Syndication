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
    def __init__(self, mode):
        '''define all aspects of configuration (datalocation hardcoded)'''
        self.notice = """
        DO NOT CHANGE THIS FILE UNLESS YOU ABSOLUTELY KNOW WHAT YOU'RE DOING
        """
        self.repositories = []
        self.platform = ''
        self.hostfile = ''
        self.patchlocation = '%s/hosts.patch' % self.datafolder
        self.defaultdomain = 'repo.ppds.me'
        self.repoobjectdict = {}
        self.repopriority = {}
        self.datafolder = ''
        self.__dict__ = self.__dict__
        self.autoconfig(mode)
        if not os.path.exists(self.datafolder):
            if mode == 'cli':
                print("Writing default data directory...")
            os.mkdir(self.datafolder)
            self.save(mode)
            self.makerepofolders()
        self.load()

    def printdict(self):
        '''debug'''
        print(self.__dict__)

    def autoconfig(self, mode):
        '''detect platform and hosts file location (windows may be wrong
        append default repo (repo.ppds.me)(pls no stealerino my domainerino)'''
        if mode == 'cli':
            print("Creating default configration file...")
        self.platform = sys.platform
        if self.platform == 'darwin' or 'linux':
            self.hostfile = '/etc/'
            self.datafolder = '~/.config/ppds/'
        elif self.platform == 'win32':
            print('windows not yet supported')
            sys.exit(1)
            # self.hostfile = '%\SystemRoot%\\System32\\drivers\\etc\\'
        else:
            self.hostfile = str(input("Enter Plaintext Hostfile Location: "))
        self.repositories.append(self.defaultdomain)

    def save(self, mode):
        '''dump config to json'''
        if (any(self.repoobjectdict) is False and
                any(self.repopriority) is False):
            if os.path.isfile('%s/config.json' % self.datafolder):
                if mode == 'cli':
                    check = str(input('Overwrite config? (y/n): '))
                    if check == 'y':
                        os.remove('config.json')
                    else:
                        return 'cancelled'
        else:
            return 'notempty'
        cfg = open('%s/config.json' % self.datafolder, 'w+')
        json.dump(self.__dict__, cfg)
        cfg.close()
        return 'created'

    def load(self):
        '''load config from config.json'''
        if os.path.isfile('%s/config.json' % self.datafolder):
            cfg = open('%s/config.json' % self.datafolder, 'r+')
            self.__dict__ = json.load(cfg)
            cfg.close()
        else:
            return 'No File'

    def makerepofolders(self):
        '''make folders for all repos in the repository list'''
        if not os.path.exists('%s/repos' % self.datafolder):
            os.mkdir('%s/repos' % self.datafolder)
        for entry in self.repositories:
            if not os.path.exists('%s/repos/%s/' % (self.datafolder, entry)):
                os.makedirs('%s/repos/%s/' % (self.datafolder, entry))

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
            shutil.rmtree('%s/repos/%s/' % (self.datafolder, repo))
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
