'''repository object'''

import json
import os


class Repository:
    ''' contains function for managing a repository entry'''
    def __init__(self, name, configuration):
        self.hosts = {}
        self.datafolder = configuration.datafolder
        self.name = (name)
        self.packages = {}
        self.priority = configuration.repopriority[name]

    def printdict(self):
        ''' debug'''
        print(self.__dict__)

    def loadpackagelist(self):
        ''' loads list of packages from file'''
        with open('%s/repos/%s/ppdslist.json' %
                  (self.datafolder, self.name), 'r+') as filevar:
            self.packages = json.load(filevar)

    def enablepackage(self, package):
        '''enables package'''
        self.packages[package] = 'enabled'

    def disablepackage(self, package):
        ''' disables package'''
        self.packages[package] = 'disabled'

    def savepackagelist(self):
        '''writes package to file'''
        if os.path.isfile('%s/repos/%s/ppdslist.json' %
                          (self.datafolder, self.name)):
            check = str(input('Overwrite ppdslist? (y/n): '))
            if check == 'y':
                os.remove('%s/repos/%s/ppdslist.json' %
                          (self.datafolder, self.name))
            else:
                return 'cancelled'
        filevar = open('%s/repos/%s/ppdslist.json' %
                       (self.datafolder, self.name), 'w+')
        json.dump(self.packages, filevar)
        filevar.close()

    def loadjson(self):
        '''loads all of the package jsons'''
        # load jsons to a nested dict to be parsed later
        for filename in os.listdir('%s/repos/%s' %
                                   (self.datafolder, self.name)):
            with open('%s/repos/%s/%s' %
                      (self.datafolder, self.name, filename), 'r+', ) as filev:
                if (filename != ".DS_Store" and
                        filename != "ppdslist.json" and
                        self.packages[filename] == 'enabled'):
                    fileproduct = json.load(filev)
                    self.hosts[filename] = fileproduct
