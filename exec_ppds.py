#!/usr/bin/env python3
import classes.config
import classes.hostfilepatch
import classes.repository
import os
import sys
UID = os.getuid()
print(os.getuid())
isRoot = False
if os.getuid() == 0:
    isRoot = True


def CheckAccess(location):
    if os.access(location, os.w_OK):
        return True
    else:
        return 'rootneeded'


def escalate(config):
    # spawn sudo command and rerun
    if isRoot:
        return 'root'
    if config.platform == 'linux' or 'darwin':
        if '.py' in sys.argv[0]:
            args = ['python3.6'] + sys.argv
        args = ['sudo'] + args
        os.execvp('sudo', args)


print(sys.argv)
testconfig = classes.config.Configuration()
escalate(testconfig)
testconfig.autoconfig()
testconfig.makerepofolders()
testconfig.save()
testconfig.load()
testconfig.addrepo('ppds.rollcagetech.com')
testconfig.forceaddrepo('ppds.rollcagetech.com')
testconfig.definerepopriority()
testconfig.initrepolist()
testconfig.repoobjectdict['repo.ppds.me'].loadpackagelist()
testconfig.repoobjectdict['ppds.rollcagetech.com'].loadpackagelist()
print(testconfig.repoobjectdict['ppds.rollcagetech.com'].packages)
testconfig.repoobjectdict['repo.ppds.me'].enablepackage('main.json')
testconfig.repoobjectdict['repo.ppds.me'].savepackagelist()
testconfig.repoobjectdict['repo.ppds.me'].loadjson()
testconfig.repoobjectdict['ppds.rollcagetech.com'].loadjson()
patcher = classes.hostfilepatch.HostPatch(testconfig)

patcher.createpatch()
patcher.patchhosts()
patcher.unpatchhosts()
