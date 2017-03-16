#!/usr/bin/env python3
import classes.config
import classes.hostfilepatch
import classes.repository
import os
import sys
UID = os.getuid()
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
            args = ['python3'] + sys.argv
        args = ['sudo'] + args
        os.execvp('sudo', args)
    else:
        return 'unsupported'


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
        print('''
Please run as your normal user so permission errors do not occur.
              ''')
        exit()
    else:
        print('''
Creating config.json with default settings''')
        newConfig.autoconfig()
        newConfig.save()
        exit()
elif '--help' in sys.argv:
    print('''
USAGE:
(in order of priority)
--version:    prints version string
--autoconfig: generates default configuration file
--root:       overrides user permission sanity checks
--help:       prints this message''')
    exit()
else:
    print('Use --help for usable arguments')
    exit()
