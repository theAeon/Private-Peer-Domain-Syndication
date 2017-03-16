import json
import classes.config
import os


class Repository:
    def __init__(self, name, configuration):
        self.hosts = {}
        self.name = (name)
        self.packages = {}
        self.priority = configuration.repopriority[name]

    def printdict(self):
        print(self.__dict__)

    def loadpackagelist(self):
        with open('repos/%s/ppdslist.json' % self.name, 'r+') as f:
            self.packages = json.load(f)

    def enablepackage(self, package):
        self.packages[package] = 'enabled'

    def disablepackage(self, package):
        self.packages[package] = 'disabled'

    def savepackagelist(self):
        if os.path.isfile('config.json'):
            check = str(input('Overwrite ppdslist? (y/n): '))
            if check == 'y':
                os.remove('repos/%s/ppdslist.json' % self.name)
            else:
                return 'cancelled'
        f = open('repos/%s/ppdslist.json' % self.name, 'w+')
        json.dump(self.packages, f)
        f.close()

    def loadjson(self):
        # load jsons to a nested dict to be parsed later
        for filename in os.listdir('repos/%s' % self.name):
            with open('repos/%s/%s' % (self.name, filename), 'r+', ) as f:
                if (filename != ".DS_Store" and
                    filename != "ppdslist.json" and
                        self.packages[filename] == 'enabled'):
                            fileproduct = json.load(f)
                            self.hosts[filename] = fileproduct
