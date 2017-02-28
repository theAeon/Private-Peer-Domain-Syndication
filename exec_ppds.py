#!/usr/bin/env python3
import classes.config, classes.hostfilepatch, classes.repository

testconfig = classes.config.Configuration()

testconfig.autoconfig()
testconfig.makerepofolders()
testconfig.save()
testconfig.load()
testconfig.addrepo('ppds.rollcagetech.com')
testconfig.forceaddrepo('ppds.rollcagetech.com')
testconfig.definerepopriority()
if testconfig.testrepo('rollcagetech.com') == 'down':
    print ('down')
testconfig.initrepolist()
testconfig.repoobjectdict['repo.ppds.me'].loadpackagelist()
testconfig.repoobjectdict['repo.ppds.me'].enablepackage('main.json')
testconfig.repoobjectdict['repo.ppds.me'].savepackagelist()
testconfig.repoobjectdict['repo.ppds.me'].loadjson()

patcher = classes.hostfilepatch.HostPatch(testconfig)

patcher.createpatch()
