#!/usr/bin/env python3
import classes.config
import classes.hostfilepatch
import classes.repository
import os
import sys
import shutil
UID = os.getuid()
isRoot = False
if os.getuid() == 0:
    isRoot = True
PermError = '''
Please run as your normal user so permission errors do not occur.
Use --root to override.
'''


def CheckAccess(location):
    if os.access(location, os.w_OK):
        return True
    else:
        return 'rootneeded'


def escalate():
    '''spawn sudo command and rerun'''
    if isRoot:
        return 'root'
    if (sys.platform == 'linux' or 'darwin' and
       shutil.which('sudo') is not None):
        if '.py' in sys.argv[0]:
            args = ['python3'] + sys.argv
        args = ['sudo'] + args
        os.execvp('sudo', args)
    else:
        return 'unsupported'

if '--root' in sys.argv and isRoot is True:
    print("Sucessfully loaded root mode.")
if '--root' in sys.argv and isRoot is False:
    print('Trying to request root privileges...')

    if escalate() == 'unsupported':
        print('''
You are not root. Please use your system\'s utilities to run this program
as root.''')
        exit(1)
if '--version' in sys.argv:
    print("""
    PPDS pre-alpha 0.0.1

    Private Peer Domain Syndication: copyright 2017 by Andrew Donshik
    Licensed under the GPL v3.0
    THIS SOFTWARE IS PROVIDED AS-IS
    WITHOUT WARRANTY OR LIABILITY AS THE LAW PERMITS
    """)
    exit(0)

elif '--autoconfig' in sys.argv:
    newConfig = classes.config.Configuration()
    if isRoot and '--root' not in sys.argv:
        print(PermError)
        exit(1)
    else:
        print('''
Creating config.json with default settings''')
        newConfig.autoconfig()
        newConfig.save()
        exit(0)
elif '--add' in sys.argv:
    config = classes.config.Configuration()
    if config.load() != 'No File':
        newrepo = str(input("Repository to add: "))
        if newrepo in config.repositories:
            print('Repo already added.')
            exit()
        if config.addrepo(newrepo) != "failure":
            if isRoot and '--root' not in sys.argv:
                print(PermError)
                exit(1)
            else:
                config.save()
                print("Added.")
                exit(0)
        else:
            print("Repository is down. Aborting.")
            exit(1)
    else:
        print("Please generate a config.json.")
elif '--forceadd' in sys.argv:
    config = classes.config.Configuration()
    if config.load() != 'No File':
        print("""
Adding repository without testing validity:
Exceptions may occur.""")
        newrepo = str(input("Repository to add: "))
        if newrepo in config.repositories:
            print('Repo already added.')
            exit(1)
        config.forceaddrepo(newrepo)
        if isRoot and '--root' not in sys.argv:
            print(PermError)
            exit(1)
        else:
            config.save()
            print("Added.")
            exit(0)
    else:
        print("Please generate a config.json.")
elif '--patch' in sys.argv:
    config = classes.config.Configuration()
    if config.load() != "No File":
        if "--root" not in sys.argv:
            print("Please restart the program with --root.")
            exit(1)
        else:
            config.initrepolist()
            for item in config.repoobjectdict:
                config.repoobjectdict[item].loadpackagelist()
                config.repoobjectdict[item].loadjson()
            patcher = classes.hostfilepatch.HostPatch(config)
            patcher.createpatch()
            if patcher.patchhosts() != "exists":
                print("Hostsfile patched sucessfully.")
                config.unloadrepolist()
                exit(0)
            else:
                print("Patcher has already been used on this hosts file.")
                config.unloadrepolist()
                exit(1)
    else:
        print("Please generate a config.json.")
elif '--unpatch' in sys.argv:
    if "--root" not in sys.argv:
        print("Please restart the program with --root.")
        exit(1)
    else:
        config = classes.config.Configuration()
        if config.load() != "No File":
            patcher = classes.hostfilepatch.HostPatch(config)
            if patcher.unpatchhosts() != "nobackup":
                print('Successfully unpatched hosts.')
                exit(0)
            else:
                print("No hostsfile backup.")
                exit(1)
elif '--help' in sys.argv:
    print('''
USAGE:
(in order of priority)
--version:    prints version string
--autoconfig: generates default configuration file
--add:        adds repository to config; checks status of repository
--forceadd:   adds repository to config without status check
--patch:      patches the hosts file of the computer (must be root)
--unpatch:    removes any patches created by ppds (must be root)
--root:       overrides user permission sanity checks and runs program as root
--help:       prints this message''')
    exit(0)
else:
    print('Use --help for usable arguments')
    exit(0)
