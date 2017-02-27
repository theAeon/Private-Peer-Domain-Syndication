import sys, json, os, requests

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
            self.hostfile = '%\SystemRoot%\\System32\\drivers\\etc\\hosts'
        else:
            self.hostfile = str(input("Enter Plaintext Hostfile Location: "))
        self.repositories.append(self.defaultdomain)
    def save(self):
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
        if os.path.isfile('config.json'):
            f = open('config.json', 'r+')
            self.__dict__ = json.load(f)
            f.close()
        else:
            return ('No File')
    def makerepofolders(self):
        if not os.path.exists('repos'):
            os.mkdir('repos')
        for entry in self.repositories:
            if not os.path.exists('repos/%s/' % entry):
                os.makedirs('repos/%s/' % entry)
    def testrepo(self, repo):
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
        if self.testrepo(repo) == 'down':
            return "failure"
        self.repositories.append(repo)
        self.makerepofolders()
        self.save()
    def forceaddrepo(self, repo):
        self.repositories.append(repo)
        self.makerepofolders()
