import sys, json, os

class Configuration:
    def __init__(self):
    	print "init"
    	self.repositories = []
        self.platform = ''
        self.hostfile = ''
    def printdict(self):
    	print self.__dict__
    def autoconfig(self):
        print sys.platform
        self.platform = sys.platform
        if self.platform == 'darwin' or 'linux2':
    	    self.hostfile = '/etc/hosts'
        elif self.platform == 'win32':
    	    self.hostfile = '%SystemRoot%\System32\drivers\etc\hosts'
        else:
            self.hostfile = str(input("Enter Plaintext Hostfile Location: "))
    def save(self):
        if os.path.isfile('config.json'):
            return('exists')
        else:
            f = open('config.json', 'w+')
            json.dump(self.__dict__, f)
            f.close()
            return('created')
            
a = Configuration()
a.autoconfig()
a.printdict()
a.save()