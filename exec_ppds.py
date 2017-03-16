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
    # spawn sudo command and rerun
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


if '--root' in sys.argv and isRoot is False:
    print('Trying to request root privileges...')

    if escalate() == 'unsupported':
        print('''
You are not root. Please use your system\'s utilities to run this program
as root.''')
        exit()
    else:
        print("Success.")
if '--version' in sys.argv:
    print("""
    PPDS pre-alpha 0.0.1

    Private Peer Domain Syndication: copyright 2017 by Andrew Donshik
    Licensed under the GPL v3.0
    THIS SOFTWARE IS PROVIDED AS-IS
    WITHOUT WARRANTY OR LIABILITY AS THE LAW PERMITS
    """)
    exit()

elif '--autoconfig' in sys.argv:
    newConfig = classes.config.Configuration()
    if isRoot and '--root' not in sys.argv:
        print(PermError)
        exit()
    else:
        print('''
Creating config.json with default settings''')
        newConfig.autoconfig()
        newConfig.save()
        exit()
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
                exit()
            else:
                config.save()
                print("Added.")
                exit()
        else:
            print("Repository is down. Aborting.")
            exit()
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
            exit()
        config.forceaddrepo(newrepo)
        if isRoot and '--root' not in sys.argv:
            print(PermError)
            exit()
        else:
            config.save()
            print("Added.")
            exit()
    else:
        print("Please generate a config.json.")

elif '--help' in sys.argv:
    print('''
USAGE:
(in order of priority)
--version:    prints version string
--autoconfig: generates default configuration file
--add:        adds repository to config; checks status of repository
--forceadd:   adds repository to config without status check
--root:       overrides user permission sanity checks and runs program as root
--help:       prints this message''')
    exit()
else:
    print('Use --help for usable arguments')
    exit()
