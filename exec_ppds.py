#!/usr/bin/env python3
import classes.config
import classes.hostfilepatch
import classes.repository

testconfig = classes.config.Configuration()

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
