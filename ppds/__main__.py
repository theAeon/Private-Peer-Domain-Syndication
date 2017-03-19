#!/usr/bin/env python3
'''main exec script'''
import sys
import ppds.instance


def exec_cli():
    '''script for pip'''
    maininstance = ppds.instance.Cli(sys.argv, 'cli')  # pylint: disable=W0612
