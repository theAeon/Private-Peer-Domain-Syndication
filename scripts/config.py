import sys, json, os

class Configuration:
    def __init__(self):
        self.repositories = []
        self.platform = ''
        self.hostfile = ''
        self.patchlocation = 'hosts.patch'
        self.defaultdomain = 'repo.ppds.me'
    def printdict(self):
        print(self.__dict__)
    def autoconfig(self):
        self.platform = sys.platform
        if self.platform == 'darwin' or 'linux2':
            self.hostfile = '/etc/hosts'
        elif self.platform == 'win32':
            self.hostfile = '%SystemRoot%\System32\drivers\etc\hosts'
        else:
            self.hostfile = str(input("Enter Plaintext Hostfile Location: "))
        self.repositories.append(self.defaultdomain)
    def save(self):
        if os.path.isfile('config.json'):
            return('exists')
        else:
            f = open('config.json', 'w+')
            json.dump(self.__dict__, f)
            f.close()
            return('created')
    def load(self):
        if os.path.isfile('config.json'):
            f = open('config.json', 'r+')
            self.__dict__ = json.load(f)
            f.close()
        else:
            return ('No File')
    def makerepofolders(self):
        if not os.path.exists('repos'):
            os.mkdir('repos')
        os.chdir('repos')
        for entry in self.repositories:
            if not os.path.exists('repos/%s/' % entry):
                os.makedirs('repos/%s/' % entry)
#class RepoConfig():
    #def __init__(self,configuration):
        #self.repositories = configuration.repositories
    #def initrepositories():
        #for repository in configuration:
            ##insert csv download script here
