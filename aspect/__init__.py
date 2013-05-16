#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

'''
    This package hold all needed aspects for an aspect orientated way of
    programming.
'''
'''
    For conventions see "boostNode/__init__.py" on
    https://github.com/thaibault/boostNode
'''

__author__ = 'Torben Sickert'
__copyright__ = 'see boostNode/__init__.py'
__credits__ = 'Torben Sickert',
__license__ = 'see boostNode/__init__.py'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python3.3 import builtins
pass
import inspect
import os
import sys

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent

# endregion

'''Determine all modules in this folder via introspection.'''
__all__ = boostNode.extension.dependent.Resolve.get_all()

# region footer

if __name__ == '__main__':
    from boostNode.extension.system import CommandLine
    CommandLine.generic_package_interface(
        name=__name__, frame=inspect.currentframe())

# endregion
