#!/usr/bin/env python3
import classes.config, classes.hostfilepatch

testconfig = classes.config.Configuration()

testconfig.autoconfig()
testconfig.makerepofolders()
testconfig.save()
testconfig.load()
testconfig.addrepo('ppds.rollcagetech.com')
testconfig.forceaddrepo('ppds.rollcagetech.com')
if testconfig.testrepo('ppds.rollcagetech.com') == 'down':
    print ('down')
patcher = classes.hostfilepatch.hostpatch(testconfig)

patcher.loadjson()
