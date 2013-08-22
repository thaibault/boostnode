#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This package provides a number of extension by dealing with often used
    things like underlying operating system, file objects, python modules,
    or I/O operations.
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
import __builtin__ as builtins
import inspect
import os
import sys

'''Make this package importable from current location.'''
for number in (3, 4):
    path = os.path.abspath(sys.path[0] + number * ('..' + os.sep))
    if not path in sys.path:
        sys.path.append(path)
if not sys.path[0]:
    sys.path[0] = os.getcwd()

# endregion

'''Determine all modules in this folder via introspection.'''
__all__ = builtins.list(builtins.set(builtins.map(
    lambda name: name[:name.rfind('.')],
    builtins.filter(
        lambda name: ((name.endswith('.py') or
                      name.endswith('.pyc')) and
                      not name.startswith('__init__.')),
        os.listdir(
            sys.path[0][:- 1 -builtins.len(os.path.basename(sys.path[0]))] if
            os.path.isfile(sys.path[0]) else sys.path[0])))))

 # region footer

'''
    Preset some variables given by introspection letting the linter know what
    globale variables are available.
'''
__logger__ = __test_mode__ = __exception__ = __module_name__ = None
if __name__ == '__main__':
    from boostNode.extension.system import CommandLine
    '''
        Extends this module with some magic environment variables to provide
        better introspection support. A generic command line interface for some
        code preprocessing tools is provided by default.
    '''
    CommandLine.generic_package_interface(
        name=__name__, frame=inspect.currentframe())

# endregion
