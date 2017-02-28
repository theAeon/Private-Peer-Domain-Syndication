import sys, json, os, requests, shutil
##everything to do with configuration in a convenient class
class Configuration:
    def __init__(self):
        # define all aspects of configuration
        self.repositories = []
        self.platform = ''
        self.hostfile = ''
        self.patchlocation = 'hosts.patch'
        self.defaultdomain = 'repo.ppds.me'
    def printdict(self):
        #debug
        print(self.__dict__)
    def autoconfig(self):
        #detect platform and hosts file location (windows may be wrong
        #append default repo (repo.ppds.me) (pls no stealerino my domainerino)
        self.platform = sys.platform
        if self.platform == 'darwin' or 'linux':
            self.hostfile = '/etc/hosts'
        elif self.platform == 'win32':
            self.hostfile = '%\SystemRoot%\\System32\\drivers\\etc\\hosts'
        else:
            self.hostfile = str(input("Enter Plaintext Hostfile Location: "))
        self.repositories.append(self.defaultdomain)
        self.makerepofolders()
    def save(self):
        #dump config to json
        if os.path.isfile('config.json'):
            check = str(input('Overwrite config? (y/n): '))
            if check == 'y':
              os.remove('config.json')
            else:
                return 'cancelled'
        f = open('config.json', 'w+')
        json.dump(self.__dict__, f)
        f.close()
        return('created')
    def load(self):
        #load config from config.json
        if os.path.isfile('config.json'):
            f = open('config.json', 'r+')
            self.__dict__ = json.load(f)
            f.close()
        else:
            return ('No File')
    def makerepofolders(self):
        #make folders for all repos in the repository list
        if not os.path.exists('repos'):
            os.mkdir('repos')
        for entry in self.repositories:
            if not os.path.exists('repos/%s/' % entry):
                os.makedirs('repos/%s/' % entry)
    def testrepo(self, repo):
        #send http request to repolist on host
        try:
            repourl = 'http://' + repo
            r = requests.get("%s/ppdslist.json" % repourl, allow_redirects=False)
        except requests.exceptions.ConnectionError:
            try:
                repourl = 'https://' + repo
                r = requests.get("%s/ppdslist.json" % repourl, allow_redirects=False)
            except requests.exceptions.ConnectionError:
                return('down')
    def addrepo(self, repo):
        #add repo to list, checking for server status
        if self.testrepo(repo) == 'down':
            return "failure"
        self.repositories.append(repo)
        self.makerepofolders()
        self.save()
    def forceaddrepo(self, repo):
        #add repo to list regardless of server status
        self.repositories.append(repo)
        self.makerepofolders()
    def removerepo(self, repo):
        if repo in self.repositories:
            self.repositories.remove(repo)
            shutil.rmtree('repos/%s/' % repo)
        else:
            return 'repo does not exist'
