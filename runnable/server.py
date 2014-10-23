#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''Provides server and request handler classes.'''

# # python3.4
# # pass
from __future__ import absolute_import, division, print_function, \
    unicode_literals
# #

'''
    For conventions see "boostNode/__init__.py" on \
    https://github.com/thaibault/boostNode
'''

__author__ = 'Torben Sickert'
__copyright__ = 'see boostNode/__init__.py'
__credits__ = 'Torben Sickert',
__license__ = 'see boostNode/__init__.py'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert["~at~"]gmail.com'
__status__ = 'stable'
__version__ = '1.0'

from base64 import b64encode as base64_encode
from base64 import b64decode as base64_decode
# # python3.4
# # import builtins
import __builtin__ as builtins
import BaseHTTPServer as server
import CGIHTTPServer
# #
import cgi
# # python3.4
# # from collections import Iterable
# # from copy import copy, deepcopy
# # from http import server
# # import imp
import Cookie as cookies
from copy import copy, deepcopy
# #
import gzip
# # python3.4 from http import cookies
pass
import inspect
# # python3.4
# # import _io
# # import io
pass
# #
import json
import logging
import multiprocessing
import os
import posixpath
# # python3.4 import socketserver
pass
import ssl
import re
import signal
import socket
import subprocess
import sys
# # python3.4
# # pass
import SocketServer
import StringIO
# #
import threading
import time
# # python3.4
# # import types
# # from urllib import parse as urlparse
import urllib
import urlparse
# #

'''Make boostNode packages and modules importable via relative paths.'''
sys.path.append(os.path.abspath(sys.path[0] + 2 * (os.sep + '..')))

# # python3.4 pass
import boostNode
from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Module, Object, \
    InstancePropertyInitializer, String
from boostNode.extension.output import Buffer, Print
from boostNode.extension.system import CommandLine, Platform, Runnable
# # python3.4 from boostNode.extension.type import Self
pass
from boostNode.paradigm.aspectOrientation import JointPoint
from boostNode.paradigm.objectOrientation import Class

# endregion


# region classes

# # python3.4
# # pass
class SocketFileObjectWrapper(socket._fileobject):

    '''
        This class wraps the native implementation of the server socket. \
        The main goal is that the first line from given socket have to be \
        taken twice. This curious feature is the only way to get the \
        requested file as early as needed to decide if we are able to \
        spawn a new process for better load balancing.
    '''

    # region dynamic methods

    # # region public

    # # # region special

    @JointPoint
    def __init__(self, *arguments, **keywords):
        '''
            This methods wraps the initializer to make the first read \
            line variable instance bounded.
        '''

        # # # region properties

        '''Indicates and saves the first line read of the socket.'''
        self.first_read_line = False

        # # # endregion

        '''Take this method via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

        # # endregion

    @JointPoint
    def readline(self, *arguments, **keywords):
        '''Wraps the "readline()" method to get the first line twice.'''
        if self.first_read_line is False:
            try:
                '''Take this method via introspection.'''
                self.first_read_line = builtins.getattr(
                    builtins.super(self.__class__, self),
                    inspect.stack()[0][3]
                )(*arguments, **keywords)
                return self.first_read_line
            except (
                socket.herror, socket.gaierror, socket.timeout,
                socket.error
            ) as exception:
                __logger__.info(
                    'Connection interrupted. %s: %s',
                    exception.__class__.__name__, builtins.str(exception))
                return ''
        elif self.first_read_line is True:
            try:
                '''Take this method via introspection.'''
                return builtins.getattr(
                    builtins.super(self.__class__, self),
                    inspect.stack()[0][3]
                )(*arguments, **keywords)
            except (
                socket.herror, socket.gaierror, socket.timeout,
                socket.error
            ) as exception:
                __logger__.info(
                    'Connection interrupted. %s: %s',
                    exception.__class__.__name__, builtins.str(exception))
                return ''
        result = self.first_read_line
        self.first_read_line = True
        return result

        # endregion

    # endregion

# #


# # python3.4
# # class MultiProcessingHTTPServer(
# #     socketserver.ThreadingMixIn, server.HTTPServer
# # ):
class MultiProcessingHTTPServer(
    SocketServer.ThreadingMixIn, server.HTTPServer, builtins.object
):
# #

    '''The Class implements a partial multiprocessing supported web server.'''

    # region dynamic methods

    # # region public

    # # # region special

    @JointPoint
# # python3.4
# #     def __init__(
# #         self: Self, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> None:
    def __init__(self, *arguments, **keywords):
# #
        '''
            This initializer wrapper makes sure that the special wrapped file \
            socket is instance bounded.
        '''

        # # # region properties

        '''
            This attribute saves the modified read file socket to apply it in \
            the request handler.
        '''
        self.read_file_socket = None

        # # # endregion

        '''Take this method via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

        # # endregion

        # endregion

    @JointPoint
# # python3.4
# #     def is_same_process_request(
# #         self: Self, request: socket.socket
# #     ) -> builtins.bool:
    def is_same_process_request(self, request):
# #
        '''
            Determines if the given request could be run in its own dedicated \
            process.
        '''
        first_request_line = self.read_file_socket.readline(
            Web.MAXIMUM_FIRST_GET_REQUEST_LINE_IN_CHARS
        ).strip()
        for pattern in self.web.same_process_request_whitelist:
# # python3.4
# #             if re.compile(pattern).fullmatch(first_request_line.decode()):
            if re.compile('(?:%s)$' % pattern).match(first_request_line):
# #
                return True
        return False

    @JointPoint
# # python3.4
# #     def process_request_no_termination_wrapper(
# #         self: Self, parent_function: types.FunctionType,
# #         request: socket.socket, arguments: builtins.tuple,
# #         keywords: builtins.dict
# #     ) -> None:
    def process_request_no_termination_wrapper(
        self, parent_function, request, arguments, keywords
    ):
# #
        '''
            Wraps the normal "process_request" method. To manage the process \
            forking stuff.
        '''
        try:
            signal_numbers = Platform.termination_signal_numbers
            for signal_number in signal_numbers:
                signal.signal(signal_number, signal.SIG_IGN)
            parent_function(self, request, *arguments, **keywords)
# # python3.4
# #         except (
# #             builtins.BrokenPipeError, socket.gaierror,
# #             socket.herror, socket.timeout, socket.error
# #         ) as exception:
        except (
            socket.herror, socket.gaierror, socket.timeout, socket.error
        ) as exception:
# #
            __logger__.info(
                'Connection interrupted. %s: %s', exception.__class__.__name__,
                builtins.str(exception))

    @JointPoint
# # python3.4
# #     def process_request(
# #         self: Self, request_socket: socket.socket,
# #         *arguments: builtins.object, **keywords: builtins.object
# #     ) -> None:
    def process_request(self, request_socket, *arguments, **keywords):
# #
        '''
            This method indicates weather the request is a read only or not. \
            Read only requests will be forked if enough free processors are \
            available.
        '''
        if self.web.block_new_worker:
            return None
# # python3.4
# #         self.read_file_socket = request_socket.makefile('rb', -1)
# #         read_file_socket = self.read_file_socket
# #
# #         @JointPoint
# #         def readline(
# #             *arguments: builtins.object, **keywords: builtins.object
# #         ) -> builtins.bytes:
# #             '''Wraps the native file object method version.'''
# #             self = read_file_socket
# #             if not builtins.hasattr(self, 'first_read_line'):
# #                 self.first_read_line = builtins.getattr(
# #                     io.BufferedReader, inspect.stack()[0][3]
# #                 )(self, *arguments, **keywords)
# #                 return self.first_read_line
# #             elif self.first_read_line is True:
# #                 '''Take this method via introspection.'''
# #                 return builtins.getattr(
# #                     io.BufferedReader, inspect.stack()[0][3]
# #                 )(self, *arguments, **keywords)
# #             result = self.first_read_line
# #             self.first_read_line = True
# #             return result
# #         self.read_file_socket.readline = readline
        '''
            This assignment replace the python's native \
            "socket.socket.makefile('rb', -1)" behavior.
        '''
        self.read_file_socket = SocketFileObjectWrapper(
            request_socket, 'rb', -1)
# #
        '''NOTE: We have to add 1 for the server processes itself.'''
        self.web.number_of_running_processes = \
            builtins.len(multiprocessing.active_children()) + 1
        parent_function = builtins.getattr(
            server.HTTPServer, inspect.stack()[0][3])
        if(not self.is_same_process_request(request_socket) and
           self.web.number_of_running_processes <
           self.web.maximum_number_of_processes):
            self.web.number_of_running_processes += 1
            '''Takes this method via introspection from now on.'''
# # python3.4
# #             multiprocessing.Process(
# #                 target=self.process_request_no_termination_wrapper,
# #                 daemon=True,
# #                 args=(parent_function, request_socket, arguments, keywords)
# #             ).start()
            forked_request_process = multiprocessing.Process(
                target=self.process_request_no_termination_wrapper,
                args=(
                    parent_function, request_socket, arguments, keywords))
            forked_request_process.daemon = True
            forked_request_process.start()
# #
        else:
            try:
# # python3.4
# #                 return parent_function(
# #                     self, request_socket, *arguments, **keywords)
# #             except (
# #                 builtins.BrokenPipeError, socket.gaierror, socket.herror,
# #                 socket.timeout, socket.error
# #             ) as exception:
                return parent_function(
                    self, request_socket, *arguments, **keywords)
            except (
                socket.herror, socket.gaierror, socket.timeout,
                socket.error
            ) as exception:
# #
                __logger__.info(
                    'Connection interrupted. %s: %s',
                    exception.__class__.__name__, builtins.str(exception))

    # endregion


class Web(Class, Runnable):

    '''
        Provides a small platform independent web server designed for easily \
        serve a client-server structure.

        **root**                                - Defines the root directory \
                                                  to be served via web.

        **host_name**                           - Defines the current host \
                                                  name. Necessary for https \
                                                  support.

        **port**                                - The port to listen for \
                                                  incoming requests. If "0" \
                                                  given a free port will be \
                                                  determined automatically.

        **default**                             - Defines a default static \
                                                  file, python module or \
                                                  dynamic executable file.

        **public_key_file**                     - Key file to support a https \
                                                  connection.

        **stop_order**                          - Standard in command to stop \
                                                  server.

        **encoding**                            - Encoding to use for \
                                                  incoming requests and \
                                                  outgoing data.

        **request_whitelist**                   - A whitelist for requests. \
                                                  All requests which doesn't \
                                                  match to one of these will \
                                                  be answered with an 404 \
                                                  error code.

        **request_blacklist**                   - A blacklist for requests to \
                                                  answer with a 404 error code.

        **same_process_request_whitelist**      - Requests which matches one \
                                                  one of theses patterns \
                                                  should be run in same \
                                                  process as the server \
                                                  itself. This is usually \
                                                  necessary if you plan to \
                                                  write in inter thread \
                                                  shared data.

        **static_mime_type_pattern**            - Defines which mime types \
                                                  should be interpreted as \
                                                  static.

        **dynamic_mime_type_pattern**           - Defines which mime types \
                                                  should be interpreted as \
                                                  dynamic.

        **compressible_mime_type_pattern**      - Defines which mime types \
                                                  could be returned in a \
                                                  compressed way.

        **default_file_name_pattern**           - Defines file name pattern \
                                                  which should be returned \
                                                  if no explicit file was \
                                                  requested.

        **default_module_names**                - Defines which module names \
                                                  should be ran if no \
                                                  explicit module was \
                                                  requested.

        **authentication**                      - Enables basic http \
                                                  authentication.

        **authentication_file_name**            - Defines file names for \
                                                  saving login data.

        **authentication_file_content_pattern** - Defines how to parse \
                                                  authentication files.

        **authentication_handler**              - A boolean function which \
                                                  decides by given request \
                                                  string and password if \
                                                  requested user is \
                                                  authenticated.

        **module_loading**                      - Enables or disables running \
                                                  python modules which are \
                                                  requested.

        **maximum_number_of_processes**         - Maximum number of used \
                                                  processor cores to use. if \
                                                  "0" is provided a useful \
                                                  number will be determined.

        **shared_data**                         - Data which will be \
                                                  available in every request \
                                                  handler instance and \
                                                  accessible for every common \
                                                  gateway interface script.

        **request_parameter_delimiter**         - Delimiter to distinguish \
                                                  requested file from given \
                                                  parameter.

        **file_size_stream_threshold_in_byte**  - Threshold which will force \
                                                  the server to stream data.

        **directory_listing**                   - Indicates weather the \
                                                  server generates a \
                                                  directory listing for \
                                                  requested directories.

        **internal_redirects**                  - A mapping of request url \
                                                  patterns to corresponding \
                                                  internal version. Regular \
                                                  expression replacements are \
                                                  supported.

        **external_redirects**                  - A mapping of request url \
                                                  patterns to corresponding \
                                                  external version. Regular \
                                                  expression replacements are \
                                                  supported.

        Examples:

        >>> Web(
        ...     maximum_number_of_processes=1, public_key_file_path='.'
        ... ) # doctest: +ELLIPSIS
        Object of "Web" with root path "...", port "0" and stop order ...

        >>> public_key_file = FileHandler(
        ...     __test_folder__.path + '_initialize_public_key_file')
        >>> public_key_file.content = ''
        >>> Web(public_key_file=public_key_file) # doctest: +ELLIPSIS
        Object of "Web" with root path "...", port "0" and stop order ...

        >>> Web(
        ...     public_key_file=__test_folder__.path
        ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ServerError: Given public key file path "..." ...
    '''

    # region properties

    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('-r', '--root'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines which path is used as web root (default is '
                     'current working directory).',
             'dest': 'root',
             'metavar': 'PATH'}},
        {'arguments': ('-H', '--host-name'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the host to bind the server to. If an empty '
                     'string (default) is given, the underlying socket will '
                     'listen on all network interfaces. E.g. a binding to the'
                     ' internal loop device "localhost" will only accept local'
                     ' requests. This makes sense if a local proxy server is '
                     'configured.',
             'dest': 'host_name',
             'metavar': 'NAME'}},
        {'arguments': ('-p', '--port'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(2 ** 16),
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the port number to access the web server. If '
                     'zero given a free port will be determined.',
             'dest': 'port',
             'metavar': 'NUMBER'}},
        {'arguments': ('-d', '--default'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines which file or module should be requested"
                            ' if nothing was declared explicitly. It could be '
                            """understood as welcome page (default: "%s").'"""
                            " % __initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'default',
             'metavar': 'PATH'}},
        {'arguments': ('-u', '--public-key-file-path'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines a public key file (*.pem) to enable open"
                            ''' ssl encryption (default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'public_key_file_path',
             'metavar': 'PATH'}},
        {'arguments': ('-o', '--stop-order'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': '"""Saves a cli-command for shutting down the '
                            'server (default: "%s").""" % '
                            '__initializer_default_value__'},
             'dest': 'stop_order',
             'metavar': 'STRING'}},
        {'arguments': ('-w', '--request-whitelist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select request type regular expression patterns which '
                     'are only allowed for being interpreted.',
             'dest': 'request_whitelist',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-b', '--request-blacklist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select request type regular expression patterns which '
                     "aren't allowed for being interpreted.",
             'dest': 'request_blacklist',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-I', '--internal-redirects'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select a mapping (with "#" as delimiter) to redirect '
                     'url suffixes internal.',
             'dest': 'internal_redirects',
             'metavar': 'REGEX_PATTERN#REPLACEMENT'}},
        {'arguments': ('-A', '--external-redirects'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select a mapping (with "#" as delimiter) to redirect '
                     'url suffixes external.',
             'dest': 'external_redirects',
             'metavar': 'REGEX_PATTERN#REPLACEMENT'}},
        {'arguments': ('-s', '--static-mime-type-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'All mime-type patterns which should recognize a "
                            'static file. Those files will be directly sent to'
                            ''' client without any preprocessing (default: '''
                            '"%s").\' % \'", "\'.join('
                            "__initializer_default_value__).replace('%', "
                            "'%%')"},
             'dest': 'static_mime_type_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-y', '--dynamic-mime-type-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'All mime-type patterns which should recognize a "
                            'dynamic file. Those files will be interpreted so '
                            'the result can be send back to client (default: '
                            '''"%s").' % '", "'.join('''
                            "__initializer_default_value__).replace('%', "
                            "'%%')"},
             'dest': 'dynamic_mime_type_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-C', '--compressible-mime-type-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'All mime-type patterns which should compressed "
                            'before sending through network socket (default: "'
                            '''%s").' % '", "'.join('''
                            "__initializer_default_value__).replace('%', "
                            "'%%')"},
             'dest': 'compressible_mime_type_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-f', '--default-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'All file name patterns which should be run if "
                            'there is one present and no other default file '
                            'pattern/name is given on initialisation (default:'
                            ''' "%s").' % '", "'.join('''
                            "__initializer_default_value__).replace('%', "
                            "'%%')"},
             'dest': 'default_file_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-n', '--default-module-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Same as file name for module name patterns. "
                            'Note that default files have a lower priority as '
                            '''default python modules (default: "%s").' % '''
                            """'", "'.join(__initializer_default_value__)"""
                            ".replace('%', '%%')"},
             'dest': 'default_module_names',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-q', '--file-size-stream-threshold-in-byte'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the minimum number of bytes which "
                            'triggers the server to send an octet-stream '
                            '''header to client (default: "%d").' % '''
                            '__initializer_default_value__'},
             'dest': 'file_size_stream_threshold_in_byte',
             'metavar': 'NUMBER'}},
        {'arguments': ('-a', '--authentication'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Enables basic http authentication. You can control '
                     'this behavior by providing an authentication file in '
                     'directories you want to save.',
             'dest': 'authentication'}},
        {'arguments': ('-e', '--enable-module-loading'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'required': False,
             'help': 'Enables module loading via get query. Enabling this '
                     'feature can slow down your request performance '
                     'extremely. Note that self module loading via "__main__" '
                     'is possible independently.',
             'dest': 'module_loading'}},
        {'arguments': ('-z', '--disable-directory-listing'),
         'keywords': {
             'action': 'store_false',
             'default': True,
             'required': False,
             'help': 'Disables automatic directory listing if a directory is '
                     'requested.',
             'dest': 'directory_listing'}},
        {'arguments': ('-g', '--authentication-file-content-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the regular expression pattern to define"
                            ' how to parse authentication files (default: '
                            '''"%s").' % __initializer_default_value__.'''
                            "replace('%', '%%')"},
             'dest': 'authentication_file_content_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-i', '--authentication-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the authentication file name (default: "
                            '''"%s").' % __initializer_default_value__.'''
                            "replace('%', '%%')"},
             'dest': 'authentication_file_name',
             'metavar': 'STRING'}},
        {'arguments': ('-j', '--request-parameter-delimiter'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the request delimiter parameter "
                            '''(default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'request_parameter_delimiter',
             'metavar': 'STRING'}},
        {'arguments': ('-E', '--encoding'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Sets encoding for interpreting binary data like "
                            'post or authentication requests, decoding given '
                            "url\\'s or encoding compressed gzip data for "
                            '''clients (default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'encoding',
             'metavar': 'STRING'}},
        {'arguments': ('-k', '--maximum-number-of-processes'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the maximum number of concurrent running"
                            ' processes. If set to zero a useful value '
                            'depending on detected processor will be '
                            '''determined (default: "%d").' % '''
                            '__initializer_default_value__'},
             'dest': 'maximum_number_of_processes',
             'metavar': 'NUMBER'}})
    '''Holds all command line interface argument informations.'''
    HIGHEST_AVAILABLE_PORT = 2 ** 16 - 1
    '''Saves the highest available port to launch server.'''
    DETERMINE_IP_SOCKET = '8.8.8.8', 80
    '''
        Globally accessible socket to ask for currently useful ip determining.
    '''
    DEFAULT_NUMBER_OF_PROCESSES = 8
    '''
        This is the maximum number of forked processes if nothing better was \
        defined or determined.
    '''
    MAXIMUM_FIRST_GET_REQUEST_LINE_IN_CHARS = 65537
    '''This values describes the longest possible first get request line.'''
    instances = []
    '''Saves all initializes server instances.'''

    # endregion

    # region dynamic methods

    # # region public

    # # # region special

    @JointPoint
# # python3.4
# #     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
# #
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Web()) # doctest: +ELLIPSIS
            'Object of "Web" with root path "...", port "0" and sto..."sto...'
        '''
        return(
            'Object of "{class_name}" with root path "{path}", port "{port}" '
            'and stop order "{stop_order}". Number of running '
            'threads/processes: {number_of_running_threads}/'
            '{number_of_running_processes}.'.format(
                class_name=self.__class__.__name__, path=self.root,
                port=self.port, stop_order=self.stop_order,
                number_of_running_threads=self.number_of_running_threads,
                number_of_running_processes=self.number_of_running_processes))

        # # endregion

    @JointPoint
# # python3.4
# #     def stop(
# #         self: Self, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> Self:
    def stop(self, *arguments, **keywords):
# #
        '''
            Waits for running workers and shuts the server down.

            Arguments and keywords are forwarded to \
            "boostNode.extension.system.Run.stop()".

            Examples:

            >>> web = Web()

            >>> web.stop() # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "0" and stop order "...

            >>> web.service = True
            >>> web.stop() # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "0" and stop order "s...
        '''
        if self.__dict__.get('service'):
            self.block_new_worker = True
            number_of_running_workers = self.number_of_running_threads + \
                builtins.len(multiprocessing.active_children())
            shown_number = 0
            while number_of_running_workers > 0:
                if(number_of_running_workers !=
                   self.number_of_running_threads +
                   builtins.len(multiprocessing.active_children())):
                    number_of_running_workers = \
                        self.number_of_running_threads + \
                        builtins.len(multiprocessing.active_children())
                if(shown_number != number_of_running_workers and
                   number_of_running_workers > 0):
                    __logger__.info(
                        'Waiting for %d running workers (%d threads and '
                        '%d processes).', number_of_running_workers,
                        self.number_of_running_threads,
                        builtins.len(multiprocessing.active_children()))
                    shown_number = number_of_running_workers
                time.sleep(2)
            __logger__.info('Shutting down web server.')
            self.__class__.instances.remove(self)
            if not __test_mode__:
                '''Terminates the serve forever loop.'''
                self.service.shutdown()
                try:
                    '''
                        Tells client site to stop writing data into the socket.
                    '''
                    self.service.socket.shutdown(socket.SHUT_RDWR)
                except socket.error as exception:
                    __logging__.warning(
                        'Connection couldn\'t be released on both sites. %s: '
                        '%s', exception.__class__.__name__, str(exception))
                '''Tells the kernel to free binded port.'''
                self.service.socket.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.service.socket.close()
        '''Take this method type by the abstract class via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

        # endregion

        # region protected

        # # region runnable implementation

    @JointPoint
# # python3.4     def _run(self: Self) -> Self:
    def _run(self):
        '''
            Entry point for command line call of this program. Starts the \
            server's request handler listing for incoming requests.

            Examples:

            >>> sys_argv_backup = copy(sys.argv)
            >>> sys.argv[1:] = ['--port', '8080']

            >>> Web()._run() # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "8080" and stop order...

            >>> sys.argv[3:] = [
            ...     '--internal-redirects', 'a#b', 'c#dd',
            ...     '--external-redirects', 'ee#f']
            >>> Web()._run() # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "8080" and stop order...

            >>> Web.run() # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "8080" and stop order...

            >>> sys.argv = sys_argv_backup
        '''
        command_line_arguments = CommandLine.argument_parser(
            arguments=self.COMMAND_LINE_ARGUMENTS,
            module_name=__name__, scope={'self': self})
        command_line_arguments.internal_redirects = builtins.tuple(
            builtins.map(
                lambda redirect: redirect.split('#'),
                command_line_arguments.internal_redirects))
        command_line_arguments.external_redirects = builtins.tuple(
            builtins.map(
                lambda redirect: redirect.split('#'),
                command_line_arguments.external_redirects))
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=command_line_arguments))

    @JointPoint(InstancePropertyInitializer)
# # python3.4
# #     def _initialize(
# #         self: Self, root=None, host_name='', port=0, default='',
# #         public_key_file=None, stop_order='stop',
# #         encoding=boostNode.ENCODING, request_whitelist=('*:/.*',),
# #         request_blacklist=(), same_process_request_whitelist=(),
# #         # NOTE: Tuple for explicit web_server file reference validation.
# #         # ('text/.+$', 'image/.+$', 'application/(x-)?javascript$')
# #         static_mime_type_pattern=('.+/.+$',),
# #         dynamic_mime_type_pattern=(
# #             'text/x-(python|sh|bash|shellscript)$',),
# #         compressible_mime_type_pattern=(
# #             'text/.+$', 'application/javascript$'),
# #         default_file_name_pattern=(
# #             '((__main__)|(main)|(index)|(initialize))(?!\.tpl$)'
# #             '(\.[a-zA-Z0-9]{0,4})?$',),
# #         default_module_names=('__main__', 'main', 'index', 'initialize'),
# #         authentication=True, authentication_file_name='.htpasswd',
# #         authentication_file_content_pattern=
# #             '(?P<name>.+):(?P<password>.+)',
# #         authentication_handler=None, module_loading=None,
# #         maximum_number_of_processes=0, shared_data=None,
# #         request_parameter_delimiter='\?',
# #         file_size_stream_threshold_in_byte=1048576,  # 1 MB
# #         directory_listing=True, internal_redirects=None,
# #         external_redirects=None, **keywords: builtins.object
# #     ) -> Self:
    def _initialize(
        self, root=None, host_name='', port=0, default='',
        public_key_file=None, stop_order='stop',
        encoding=boostNode.ENCODING, request_whitelist=('*:/.*',),
        request_blacklist=(), same_process_request_whitelist=(),
        # NOTE: Tuple for explicit web_server file reference validation.
        # ('text/.+$', 'image/.+$', 'application/(x-)?javascript$')
        static_mime_type_pattern=('.+/.+$',),
        dynamic_mime_type_pattern=(
            'text/x-(python|sh|bash|shellscript)$',),
        compressible_mime_type_pattern=(
            'text/.+$', '^application/javascript$'),
        default_file_name_pattern=(
            '((__main__)|(main)|(index)|(initialize))(?!\.tpl$)'
            '(\.[a-zA-Z0-9]{0,4})?$',),
        default_module_names=('__main__', 'main', 'index', 'initialize'),
        authentication=True, authentication_file_name='.htpasswd',
        authentication_file_content_pattern=
            '(?P<name>.+):(?P<password>.+)',
        authentication_handler=None, module_loading=None,
        maximum_number_of_processes=0, shared_data=None,
        request_parameter_delimiter='\?',
        file_size_stream_threshold_in_byte=2097152,  # 2 MB
        directory_listing=True, internal_redirects=None,
        external_redirects=None, **keywords
    ):
# #
        '''
            Sets root path of web server and all properties. Although the \
            server thread will be started.
        '''
        self.__class__.instances.append(self)

        # # # region properties

        if self.internal_redirects is None:
            self.internal_redirects = ()
        if self.external_redirects is None:
            self.external_redirects = ()
        '''Indicates if new worker are currently allowed to spawn.'''
        self.block_new_worker = False
        '''Saves server runtime properties.'''
        self.root = FileHandler(location=self.root)
        self.thread_buffer = Buffer(queue=True)
        '''Saves the number of running threads.'''
        self.number_of_running_threads = 0
        '''Saves the server thread service.'''
        self.service = None
        '''
            Saves the number of running process forked by this server instance.
        '''
        self.number_of_running_processes = 0
        if Platform.operating_system == 'windows':
            self.maximum_number_of_processes = 1
        elif not self.maximum_number_of_processes:
            try:
                self.maximum_number_of_processes = \
                    2 * multiprocessing.cpu_count()
            except builtins.NotImplementedError:
                self.maximum_number_of_processes = \
                    self.DEFAULT_NUMBER_OF_PROCESSES
        '''
            Saves informations how to define authentications in protected \
            directories.
        '''
        if self.public_key_file:
            self.public_key_file = FileHandler(location=self.public_key_file)
            if not self.public_key_file.is_file():
                raise __exception__(
                    'Given public key file path "%s" doesn\'t points to a '
                    'file.', self.public_key_file._path)

                # endregions

        return self._start_server_thread()

        # # endregion

    @JointPoint
# # python3.4     def _start_server_thread(self: Self) -> Self:
    def _start_server_thread(self):
        '''
            Starts the server's request handler instance and listens for \
            shutting-down-command.
        '''
        if self.port:
            self._start_with_static_port()
        else:
            self._start_with_dynamic_port()
        self._log_server_status()
        if not __test_mode__ and self.stop_order:
            self.wait_for_order()
        return self

    @JointPoint
# # python3.4     def _log_server_status(self: Self) -> Self:
    def _log_server_status(self):
        '''Prints some information about the way the server was started.'''
        determine_ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.gethostbyname(socket.gethostname())
        if self.host_name == '':
            try:
                determine_ip_socket.connect(self.DETERMINE_IP_SOCKET)
# # python3.4
# #             except (
# #                 builtins.BrokenPipeError, socket.gaierror, socket.herror,
# #                 socket.timeout, socket.error
# #             ) as exception:
            except (
                socket.herror, socket.gaierror, socket.timeout,
                socket.error
            ):
# #
                pass
            else:
                ip = determine_ip_socket.getsockname()[0]
            finally:
                try:
                    determine_ip_socket.shutdown(socket.SHUT_RDWR)
                except socket.error:
                    pass
                determine_ip_socket.close()
        __logger__.info(
            'Web server is starting%s, listens at port "%d" and webroot is '
            '"%s". Currently reachable ip is "%s". Maximum parallel processes '
            'is limited to %d.', (
                ' a secure connection with public key "%s" ' %
                self.public_key_file._path
            ) if self.public_key_file else '', self.port, self.root._path,
            ip, self.maximum_number_of_processes)
        return self

    @JointPoint
# # python3.4     def _start_with_dynamic_port(self: Self) -> Self:
    def _start_with_dynamic_port(self):
        '''Searches for the highest free port for listing.'''
        ports = [
            80, 8080, 8008, 8090, 8280, 8887, 9080, 16080, 3128, 4567,
            5000, 4711, 443, 5001, 5104, 5800, 8243, 8888]
        if self.public_key_file:
            ports = [443] + ports
        ports += builtins.list(builtins.set(
            builtins.range(self.HIGHEST_AVAILABLE_PORT)
        ).difference(ports))
        if not __test_mode__:
            for port in ports:
                try:
                    self._initialize_server_thread(port)
                except socket.error:
                    if port == self.HIGHEST_AVAILABLE_PORT:
# # python3.4
# #                         raise __exception__(
# #                             'No port is available to run the web-server '
# #                             'with given rights.'
# #                         ) from None
                        raise __exception__(
                            'No port is available to run the web-server '
                            'with given rights.')
# #
                else:
                    self.port = port
                    return self
        return self

    @JointPoint
# # python3.4     def _start_with_static_port(self: Self) -> Self:
    def _start_with_static_port(self):
        '''Starts the server listing on the given port, if it is free.'''
        if not __test_mode__:
            try:
                self._initialize_server_thread(port=self.port)
            except socket.error:
# # python3.4
# #                 raise __exception__(
# #                     "Port %d isn't available to run the web-server with "
# #                     'given rights.', self.port
# #                 ) from None
                raise __exception__(
                    "Port %d isn't available to run the web-server with "
                    'given rights.', self.port)
# #
        return self

    @JointPoint
# # python3.4
# #     def _serve_service_forever_exception_catcher(self: Self) -> Self:
    def _serve_service_forever_exception_catcher(self):
# #
        '''
            This method wraps the python's native server "serve_forever()" \
            method to handle incoming exceptions in a separat thread.
        '''
        try:
            return self.service.serve_forever()
# # python3.4         except builtins.ValueError as exception:
        except socket.error as exception:
            __logger__.warning(
                '%s: %s', exception.__class__.__name__,
                builtins.str(exception))
        return self

    @JointPoint
# # python3.4
# #     def _initialize_server_thread(
# #         self: Self, port: builtins.int
# #     ) -> Self:
    def _initialize_server_thread(self, port):
# #
        '''Initializes a new request-handler and starts its own thread.'''
        self.service = MultiProcessingHTTPServer(
            (self.host_name, port), CGIHTTPRequestHandler)
        if self.public_key_file:
            self.service.socket = ssl.wrap_socket(
                self.service.socket, certfile=self.public_key_file._path,
                server_side=True)
        self.service.web = self
# # python3.4
# #         threading.Thread(
# #             target=self._serve_service_forever_exception_catcher,
# #             daemon=True
# #         ).start()
        server_thread = threading.Thread(
            target=self._serve_service_forever_exception_catcher)
        server_thread.daemon = True
        server_thread.start()
# #
        return self

        # endregion

    # endregion


# # python3.4
# # class CGIHTTPRequestHandler(server.CGIHTTPRequestHandler):
class CGIHTTPRequestHandler(
    CGIHTTPServer.CGIHTTPRequestHandler, builtins.object
):
# #

    '''
        A small request-handler dealing with incoming file requests. It can \
        directly send static files back to client or run dynamic scripts and \
        give the output back to client.
    '''

    # region dynamic methods

    # # region public

    # # # region special

    @JointPoint
# # python3.4
# #     def __init__(
# #         self, *arguments: builtins.object, **keywords: builtins.object
# #     ) -> None:
# #         '''
# #             This method calls is parent. It's necessary to make some class
# #             properties instance properties.
# #         '''
    def __init__(self, *arguments, **keywords):
# #
        '''
            Initializes all used properties and calls the super method.

            Examples:

            >>> CGIHTTPRequestHandler() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''

        # # # region properties

        '''Properties defined by incoming request.'''
        self.host = ''
        self.request_uri = ''
        self.external_request_uri = ''
        self.parameter = ''
        self.get = {}
        self.data = {}
        self.cookie = {}
        self.request_type = ''
        self.external_request_type = ''
        self.data_type = ''
        self.last_running_worker = None
        '''Saves the last started worker thread instance.'''
        self.requested_file_name = ''
        '''
            Consists the explicit requested file name (like python's native \
            "self.file") coming from client.
        '''
        self.requested_file = None
        '''References the corresponding file handler to requested file name.'''
        self.load_module = False
        '''
            Defines weather the handler has decided to run a python module or \
            an external script.
        '''
        self.request_arguments = []
        '''
            Defines arguments given to a requested file which is running by \
            the server.
        '''
        self.respond = False
        '''Indicates if an answer is expected from the requested file.'''
        self.response_sent = self.headers_ended = self.content_type_sent = \
            self.content_length_sent = False
        '''Saves the error message format.'''
# # python3.4         self.error_message_format = (
        self.error_message_format = builtins.str(
            '<!DOCTYPE html>\n'
            '<html>\n'
            '\t<head><title>Error response</title></head>\n'
            '\t<body>\n'
            '\t\t<h1>Error response</h1>\n'
            '\t\t<p>Error code %(code)d.</p>\n'
            '\t\t<p>Message:</p>\n'
            '\t\t<pre>%(message)s.</pre>\n'
            '\t\t<p>Error code explanation: %(code)s</p>\n'
            '\t\t<p>%(explain)s.</p>\n'
            '\t</body>\n'
            '</html>')
        self.server_version = '{program} {version} {status}'.format(
            program=String(__module_name__).get_camel_case_capitalize(
            ).content, version=__version__, status=__status__)
        '''
            Saves the self describing server version string. This string is \
            included in every response.
        '''
        self._encoded_output = None
        '''Saves gziped encoded output.'''
        self._authentication_location = None
        '''
            Points to location which is authoritative to be reachable from \
            requested destination.
        '''

        # # # endregion

        if not __test_mode__:
            '''Take this method via introspection.'''
            return builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(*arguments, **keywords)

    @JointPoint
# # python3.4     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(CGIHTTPRequestHandler()) # doctest: +SKIP
            'Object of "CGIHTTPRequestHandler" with request uri "" and para...'
        '''
        return 'Object of "{class_name}" with request uri "{url}" and '\
               'parameter "{parameter}".'.format(
                   class_name=self.__class__.__name__, url=self.request_uri,
                   parameter=self.parameter)

        # # endregion

        # # region event

    @JointPoint
# # python3.4     def do_GET(self: Self) -> Self:
    def do_GET(self):
        '''
            Is triggered if an incoming get request is detected. Decides if \
            request is valid and static or dynamic. It also through an \
            exception and sends an http-error if request isn't valid.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/" and param...

            >>> handler.path = ''
            >>> handler.server.web.directory_listing = False
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.server.web.authentication = True
            >>> handler.server.web.authentication_handler = (
            ...     lambda login_data, request_handler: False)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('key: value'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('key', 'value')
            >>> # #
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String(
            ...             'Authorization: Basic ' +
            ...             base64_encode('hans:hans')
            ...         ), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header(
            ...         'Authorization',
            ...         'Basic ' + base64_encode(b'hans:hans').decode(
            ...             handler.server.web.encoding))
            >>> # #
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('authorization: value'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('authorization', 'value')
            >>> # #
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> handler.path = '/not_existing_file'
            >>> handler.server.web.request_whitelist = '*:/not_existing_file',
            >>> handler.server.web.authentication_handler = (
            ...     lambda login_data, request_handler: True)
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/not_existin...

            >>> file = FileHandler(__test_folder__.path + 'do_GET')
            >>> file.content = ''
            >>> handler.path = '/' + file.name
            >>> handler.server.web.request_whitelist = '*:/%s' % file.name,
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/do_GET" ...

            >>> handler.path = 'not_in_whitlist'
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "not_in_whitl...

            >>> handler.server.web.request_whitelist = '*:/%s' % file.name,
            >>> handler.path = '/do_GET'
            >>> handler.server.web.external_redirects = (('GET:.*', ''),)
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/do_GET" ...

            >>> handler.server.web.request_whitelist = '*:/%s' % file.name,
            >>> handler.path = '/do_GET'
            >>> handler.server.web.external_redirects = (('POST:.*', ''),)
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/do_GET" ...

            >>> handler.server.web.external_redirects = (
            ...     ('*:(.+)', '/\\\\1/'),)
            >>> handler.path = '/do_GET'
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/do_GET" ...

            >>> handler.server.web.internal_redirects = (
            ...     ('*:(.+)', '-:\\\\1/'),)
            >>> handler.path = '/do_GET'
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/do_GET/" ...

            >>> handler.path = __test_folder__.path
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/..." ...

            >>> handler.server.web.internal_redirects = (
            ...     ('*:(.+)', 'PUT:\\\\1/'),)
            >>> handler.path = '/do_GET'
            >>> handler.do_GET() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/do_GET/" ...
        '''
        self.external_request_type = self.request_type = \
            self.request_type if self.request_type else 'get'
        self._create_environment_variables()
        if self._is_authenticated():
            valid_request = self._is_valid_request()
            if valid_request:
                if self._handle_redirect():
                    return self
                if self.path:
                    if self._is_valid_reference():
                        return self._set_dynamic_or_static_get(
                            file_name=self.path)
                elif self._default_get():
                    return self
            return self._send_no_file_error(valid_request)
        return self._send_no_authorization_error()

    @JointPoint
# # python3.4     def do_POST(self: Self) -> Self:
    def do_POST(self):
        '''
            Is triggered if a post request is coming.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.do_POST() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/" and param...
        '''
        return self._do_data_request(type=inspect.stack()[0][3])

    @JointPoint
# # python3.4     def do_PATCH(self: Self) -> Self:
    def do_PATCH(self):
        '''
            Is triggered if a patch request is coming.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.do_PATCH() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/" and param...
        '''
        return self._do_data_request(type=inspect.stack()[0][3])

    @JointPoint
# # python3.4     def do_DELETE(self: Self) -> Self:
    def do_DELETE(self):
        '''
            Is triggered if a delete request is coming.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.do_DELETE() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/" and param...
        '''
        return self._do_data_request(type=inspect.stack()[0][3])

    @JointPoint
# # python3.4     def do_PUT(self: Self) -> Self:
    def do_PUT(self):
        '''
            Is triggered if a put request is coming.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.do_PUT() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/" and param...
        '''
        return self._do_data_request(type=inspect.stack()[0][3])

    @JointPoint
# # python3.4     def do_HEAD(self: Self) -> Self:
    def do_HEAD(self):
        '''
            Is triggered if a head request is coming.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.do_HEAD() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "/" and param...
        '''
        self.request_type = inspect.stack()[0][3][builtins.len('do_'):].lower()
        return self.do_GET()

        # # endregion

    @JointPoint
# # python3.4     def parse_url(self: Self, url=None) -> builtins.tuple:
    def parse_url(self, url=None):
        '''
            This method provides an easy way to split a http request string \
            into its components.

            **url** - URL to parse.

            Returns a tuple containing of the parse object and a dictionary \
            containing get parameter.

            >>> sys_argv_backup = copy(sys.argv)
            >>> handler = CGIHTTPRequestHandler()
            >>> handler.request_parameter_delimiter = '?'
            >>> sys.argv = sys.argv[:1]

            >>> handler.parse_url()
            (None, {})

            >>> sys.argv[1:] = ['hans']
            >>> handler.server = Class()
            >>> handler.server.web = Web()
            >>> handler.parse_url() # doctest: +ELLIPSIS
            (ParseResult(...'hans'...), {})

            >>> sys.argv[1:] = ['?hans=peter']
            >>> handler.server = Class()
            >>> handler.server.web = Web()
            >>> handler.parse_url() # doctest: +ELLIPSIS
            (ParseResult(..., {'hans': 'peter'})

            >>> sys.argv[1:] = ['?hans=peter&s']
            >>> handler.server = Class()
            >>> handler.server.web = Web()
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> handler.parse_url() # doctest: +ELLIPSIS
            (ParseResult(...'hans=peter&s'...})
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '... "?hans=peter&s" is not a valid get query string.\\n'

            >>> sys.argv = sys_argv_backup
        '''
        if url is None and builtins.len(sys.argv) > 1:
            url = sys.argv[1]
        if url:
            url = re.compile(
                self.server.web.request_parameter_delimiter
            ).sub('?', url, 1)
            get = urlparse.urlparse(url).query
            if get:
                try:
# # python3.4
# #                     get = urlparse.parse_qs(
# #                         qs=get, keep_blank_values=True,
# #                         strict_parsing=True,
# #                         encoding=self.server.web.encoding,
# #                         errors='replace')
                    get = urlparse.parse_qs(
                        qs=get, keep_blank_values=True, strict_parsing=True
                    )
# #
                except builtins.ValueError:
                    get = {}
                    __logger__.info(
                        '"%s" is not a valid get query string.', url)
            if not get:
                get = {}
            for key, value in get.items():
                get[key] = value[0]
            return urlparse.urlparse(url), get
        return None, {}

    @JointPoint
# # python3.4
# #     def send_response(
# #         self: Self, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> Self:
    def send_response(self, *arguments, **keywords):
# #
        '''
            Send the given response code to client if no response code was \
            sent yet.

            Examples:

            >>> CGIHTTPRequestHandler().send_response() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        if not (self.response_sent or __test_mode__):
            if builtins.len(arguments) > 1 and builtins.isinstance(
                arguments[1], builtins.str
            ):
                arguments = builtins.list(arguments)
                arguments[1] = arguments[1].replace('\n', '\\n')
                arguments = builtins.tuple(arguments)
            self.response_sent = True
            '''Take this method via introspection.'''
            builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(*arguments, **keywords)
        return self

    @JointPoint
# # python3.4
# #     def send_error(
# #         self: Self, code: builtins.int, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> Self:
    def send_error(self, code, *arguments, **keywords):
# #
        '''
            Send the given error to client if no response code was sent yet.

            **code** - Error code to send.
        '''
        if not (self.response_sent or __test_mode__):
            self.content_type_sent = self.content_length_sent = True
            self.send_response(code)
            '''Take this method via introspection.'''
            builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(code, *arguments, **keywords)
        return self

    @JointPoint
# # python3.4
# #     def list_directory(
# #         self: Self, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> Self:
    def list_directory(self, *arguments, **keywords):
# #
        '''
            Generates a simple html web page listing requested directory \
            content.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.path = '/'
            >>> handler.server = Class()
            >>> handler.server.web = Web(
            ...     __test_folder__, request_whitelist=('*:/?',))
            >>> handler.requested_file = FileHandler()

            >>> handler.list_directory() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and param...
        '''
        path_backup = self.path
        self.path = self.requested_file.path[builtins.len(
            self.server.web.root.path
        ) - builtins.len(os.sep):]
        '''Take this method via introspection.'''
        if not __test_mode__:
            file_handler = builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(self.requested_file._path, *arguments, **keywords)
            self._send_output(output=file_handler)
        self.path = path_backup
        return self

    @JointPoint
# # python3.4
# #     def end_headers(
# #         self: Self, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> Self:
    def end_headers(self, *arguments, **keywords):
# #
        '''Finishes all sent headers by a trailing new empty line.'''
        if not (self.headers_ended or __test_mode__):
            self.headers_ended = True
            '''Take this method via introspection.'''
            builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(*arguments, **keywords)
        return self

    @JointPoint
# # python3.4
# #     def send_static_file_cache_header(
# #         self: Self, timestamp=time.time(), response_code=200,
# #         cache_control_header='public, max-age=0', expire_time_in_seconds=0
# #     ) -> Self:
    def send_static_file_cache_header(
        self, timestamp=time.time(), response_code=200,
        cache_control_header='public, max-age=0', expire_time_in_seconds=0
    ):
# #
        '''
            Response a static file-request header.

            **timestamp**              - Timestamp to use as last modified \
                                         time.

            **response_code**          - Response code to send if not sent yet.

            **cache_control_header**   - Cache control header string.

            **expire_time_in_seconds** - Additional time to current timestamp \
                                         for expires header.
        '''
        if not __test_mode__:
            self.send_response(response_code).send_header(
                'Cache-Control', cache_control_header)
            self.send_header('Last-Modified', self.date_time_string(timestamp))
            self.send_header('Expires', self.date_time_string(
                timestamp + expire_time_in_seconds))
        return self

    @JointPoint
# # python3.4
# #     def get_cookie(
# #         self: Self, name=None
# #     ) -> (builtins.str, cookies.SimpleCookie, builtins.type(None)):
    def get_cookie(self, name=None):
# #
        '''
            Retrieves a http cookie.

            **name** - If provided only the matching value will be returned \
                       instead of the whole cookie object.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('hans: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('hans', 'hans')
            >>> # #

            >>> handler.get_cookie() # doctest: +ELLIPSIS

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('Cookie: hans=hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('Cookie', 'hans=hans')
            >>> # #

            >>> handler.get_cookie() # doctest: +ELLIPSIS
            <SimpleCookie: hans='hans'>

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('Cookie: ha/ns=hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('Cookie', 'ha/ns=hans')
            >>> # #

            >>> handler.get_cookie() # doctest: +ELLIPSIS
            <SimpleCookie: hans='hans'>

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...WARNING - Invalid cookie detected "ha/ns=hans". ...'

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('Cookie: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('Cookie', 'hans')
            >>> # #

            >>> handler.get_cookie() # doctest: +ELLIPSIS
            <SimpleCookie: >

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            ''

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('Cookie: hans='), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('Cookie', 'hans=')
            >>> # #

            >>> handler.get_cookie() # doctest: +ELLIPSIS
            <SimpleCookie: hans=''>

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            ''

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('Cookie: h/a//ns////=ha/ns'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('Cookie', 'h/a//ns////=ha/ns')
            >>> # #

            >>> handler.get_cookie() # doctest: +ELLIPSIS
            <SimpleCookie: hans='ha/ns'>

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...WARNING - Invalid cookie detected ...'
        '''
# # python3.4         if 'cookie' in self.headers:
        if self.headers.get('cookie'):
            cookie = cookies.SimpleCookie()
            cookie_content = self.headers.get('cookie')
            while True:
                try:
                    cookie.load(cookie_content)
                except cookies.CookieError as exception:
                    new_cookie_content = re.compile(
                        '([^=]*)/+([^=]*=[^;]*(?:;|$))'
                    ).sub('\\1\\2', cookie_content)
                    if cookie_content == new_cookie_content:
                        __logger__.critical(
                            'Invalid cookie detected "%s". %s: %s',
                            cookie_content, exception.__class__.__name__, str(
                                exception))
                        return None
                    else:
                        __logger__.warning(
                            'Invalid cookie detected "%s". %s: %s. Trying "%s"'
                            '.', cookie_content, exception.__class__.__name__,
                            builtins.str(exception), new_cookie_content)
                        cookie_content = new_cookie_content
                else:
                    break
            return cookie[name].value if name and name in cookie else cookie
        return None

    @JointPoint
# # python3.4
# #     def send_cookie(
# #         self: Self,
# #         cookie: (cookies.SimpleCookie, builtins.str, builtins.dict),
# #         header='Set-Cookie', maximum_age_in_seconds=60 * 60 * 24 * 7,
# #         version=1, domain='', secure=False, httponly=False, comment='',
# #         path='/', response_code=200
# #     ) -> Self:
    def send_cookie(
        self, cookie, header='Set-Cookie',
        maximum_age_in_seconds=60 * 60 * 24 * 7, version=1, domain='',
        secure=False, httponly=False, comment='', path='/',
        response_code=200
    ):
# #
        '''
            Sends a http cookie.

            **cookie**                 - Cookie object, dictionary or string.

            **header**                 - HTTP Header to use.

            **maximum_age_in_seconds** - Maximum age of given cookie. Default \
                                         is 7 days.

            **version**                - Given cookie version.

            **domain**                 - The domain the cookie should bounded \
                                         to.

            **secure**                 - Indicates weather only secure \
                                         connections should be associated \
                                         with given cookie.

            **httponly**               - Disables JavaScript access to given \
                                         cookie.

            **comment**                - A comment provided for given cookie.

            **path**                   - Web path the cookie should bounded to.

            **response_code**          - Response code to send if not sent yet.

            Examples:

            >>> handler = CGIHTTPRequestHandler()

            >>> handler.send_cookie('') # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.send_cookie('key=value;a=1') # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.send_cookie({}) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> if sys.version_info.major < 3:
            ...     handler.send_cookie(
            ...         {str('key'): str('value'), str('a'): 1}
            ...     ) # doctest: +ELLIPSIS
            ... else:
            ...     handler.send_cookie({'key': 'value', 'a': 1})
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> cookie = cookies.SimpleCookie()
            >>> if sys.version_info.major < 3:
            ...     cookie[str('key')] = str('value')
            ...     cookie[str('a')] = 1
            ... else:
            ...     cookie['key'] = 'value'
            ...     cookie['a'] = 1
            >>> handler.send_cookie(cookie) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        if not builtins.isinstance(cookie, cookies.SimpleCookie):
            cookie_object = cookies.SimpleCookie()
# # python3.4
# #             if builtins.isinstance(cookie, builtins.str):
            if builtins.isinstance(cookie, (
                builtins.unicode, builtins.str
            )):
# #
                cookie_object.load(cookie_object)
            else:
                for key, value in cookie.items():
                    cookie_object[key] = value
            cookie = cookie_object
        expires = self.date_time_string(time.time() + maximum_age_in_seconds)
        cookie = re.compile('^[^:]+: *').sub('', cookie.output()) + (
            ';version="%s";expires=%s;Max-Age=%d;Path=%s;comment=%s;'
            'domain=%s%s%s' % (
                builtins.str(version), expires, maximum_age_in_seconds, path,
                comment, domain, ';secure' if secure else '',
                ';httponly' if httponly else ''))
        if not __test_mode__:
            self.send_response(response_code).send_header(header, cookie)
        return self

    @JointPoint
# # python3.4
# #     def send_content_type_header(
# #         self: Self, mime_type='text/html', encoding=None,
# #         response_code=200
# #     ) -> Self:
    def send_content_type_header(
        self, mime_type='text/html', encoding=None, response_code=200
    ):
# #
        '''
            Sends a content type header to client if not sent yet.

            **mime_type**     - Mime type to send to client.

            **encoding**      - Encoding description to send to client.

            **response_code** - HTTP Response code to send.

            Additional arguments and keywords will be forwarded to \
            "self.send_header()" method.
        '''
        if not (self.content_type_sent or __test_mode__):
            self.content_type_sent = True
            self.send_response(response_code)
            self.send_header('Content-Type', '%s; charset=%s' % (
                mime_type, (
                    self.server.web.encoding if encoding is None else encoding
                ).replace('_', '-')))
        return self

    @JointPoint
# # python3.4
# #     def send_content_length_header(
# #         self: Self, size: builtins.int, dynamic_output='',
# #         response_code=200
# #     ) -> Self:
    def send_content_length_header(
        self, size, dynamic_output='', response_code=200
    ):
# #
        '''
            Sends the content length header to client if not sent yet.

            **size**           - Content length to send.

            **dynamic_output** - Indicates weather output should be forced to \
                                 compressed because it is simply a computed \
                                 string.

            **response_code**  - HTTP Response code to send.
        '''
        if not (self.content_length_sent or __test_mode__):
            self.content_length_sent = True
            self.send_response(response_code)
            threshold = self.server.web.file_size_stream_threshold_in_byte
# # python3.4
# #             if(size < threshold and
# #                'accept-encoding' in self.headers and
# #                gzip.__name__ in self.headers.get('accept-encoding').split(
# #                    ','
# #                ) and (dynamic_output or self._check_pattern(
# #                    patterns=self.server.web.compressible_mime_type_pattern,
# #                    subject=self.requested_file.mime_type))):
            if(size < threshold and
               self.headers.get('accept-encoding', False) and
               gzip.__name__ in self.headers.get(
                   'accept-encoding'
               ).split(',') and
               (dynamic_output or self._check_pattern(
                   patterns=self.server.web.compressible_mime_type_pattern,
                   subject=self.requested_file.mime_type))):
# #
                self.send_header('Content-Encoding', gzip.__name__)
                if dynamic_output:
                    self._encoded_output = self._gzip(content=dynamic_output)
                else:
                    self._encoded_output = self._gzip(
                        content=self.requested_file.content)
                self.send_header('Content-Length', builtins.len(
                    self._encoded_output))
            else:
                self.send_header('Content-Length', size)
        return self

    @JointPoint
# # python3.4
# #     def log_message(
# #         self: Self, format: builtins.str,
# #         message_or_error_code: (builtins.int, builtins.str),
# #         response_code_or_message: (builtins.str, builtins.int),
# #         message_end=None
# #     ) -> Self:
    def log_message(
        self, format, message_or_error_code, response_code_or_message,
        message_end=None
    ):
# #
        '''
            Wrapper method for all logging output coming through the server \
            thread.

            **format**                   - Logging format. Allowed \
                                           placeholder are: "client_ip", \
                                           "client_port", \
                                           "request_description", \
                                           "response_code", "forwarded_ip", \
                                           "forwarded_host", \
                                           "forwarded_server", \
                                           "forwarded_server" and \
                                           "server_port".

            **message_or_error_code**    - Logging message or resulting HTTP \
                                           code.

            **response_code_or_message** - Resulting HTTP code or response \
                                           message.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web()
            >>> handler.client_address = '192.168.0.1', 80

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> handler.log_message('', 404, '') # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...404...'

            >>> handler.server.web.__class__.instances = [handler.server.web]
            >>> handler.log_message('', 404, '') # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.log_message('', '', 404) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('key: value'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('key', 'value')
            >>> # #
            >>> handler.log_message('', '', 404) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(String(
            ...         'x-forwarded-for: 192.168.0.1\\n'
            ...         'x-forwarded-host: 192.168.0.1\\n'
            ...         'x-forwarded-server: 192.168.0.1'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header(
            ...         'x-forwarded-for', '192.168.0.1')
            ...     handler.headers.add_header(
            ...         'x-forwarded-host', '192.168.0.1')
            ...     handler.headers.add_header(
            ...         'x-forwarded-server', '192.168.0.1')
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> handler.log_message('', '', 404) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...192.168.0.1:80  -> 404 - forwarded for: 192.168.0.1 - forwar...
        '''
        format = (
            '{client_ip}:{client_port} {request_description} -> '
            '{response_code}')
        forwarded_ip = forwarded_host = forwarded_server = None
        if 'headers' in self.__dict__:
            forwarded_ip = self.headers.get('x-forwarded-for')
            forwarded_host = self.headers.get('x-forwarded-host')
            forwarded_server = self.headers.get('x-forwarded-server')
            if forwarded_ip:
                format += ' - forwarded for: {forwarded_ip}'
            if forwarded_host:
                format += ' - forwarded host: {forwarded_host}'
            if forwarded_server:
                format += ' - forwarded server: {forwarded_server}'
        if builtins.len(self.server.web.__class__.instances) > 1:
            format += ' (server port: {server_port})'
        request_description = message_or_error_code
        response_code = response_code_or_message
        if builtins.isinstance(message_or_error_code, builtins.int):
            request_description = response_code_or_message
            response_code = message_or_error_code
# # python3.4
# #         pass
        if builtins.isinstance(request_description, builtins.str):
            request_description = builtins.unicode(
                request_description, boostNode.ENCODING)
# #
        __logger__.info(format.format(
            client_ip=self.client_address[0],
            client_port=self.client_address[1],
            request_description=request_description,
            response_code=response_code, forwarded_ip=forwarded_ip,
            forwarded_host=forwarded_host, forwarded_server=forwarded_server,
            server_port=self.server.web.port))
        return self

    @JointPoint
# # python3.4
# #     def setup(
# #         self: Self, *arguments: builtins.object,
# #         **keywords: builtins.object
# #     ) -> None:
    def setup(self, *arguments, **keywords):
# #
        '''
            This method wraps the python's native request handler to provide \
            our wrapped file socket buffer.
        '''
        '''Take this method via introspection.'''
        result = builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)
        self.rfile = self.server.web.service.read_file_socket
        return result

        # endregion

        # region protected

        # # region boolean

    @JointPoint
# # python3.4     def _is_authenticated(self: Self) -> builtins.bool:
    def _is_authenticated(self):
        '''
            Determines weather current request is authenticated.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler._authentication_location = __test_folder__
            >>> handler._is_authenticated()
            True

            >>> file = FileHandler(
            ...     __test_folder__.path + '_is_authenticated',
            ...     make_directory=True)
            >>> handler.path = '/' + file.name
            >>> handler._create_environment_variables()
            '_is_authenticated'
            >>> handler._is_authenticated()
            True

            >>> FileHandler(file.path + '.htpasswd').content = 'login:password'
            >>> handler.path = '/' + file.name
            >>> handler._create_environment_variables()
            '_is_authenticated'
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('key: value'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('key', 'value')
            >>> # #
            >>> handler._is_authenticated()
            False

            >>> handler.server.web.authentication_file_name = ''
            >>> handler._is_authenticated()
            True

            >>> handler.server.web.authentication = False
            >>> handler._is_authenticated()
            True
        '''
        if self.server.web.authentication:
            while self.server.web.authentication_file_name:
                file_path = (
                    self._authentication_location.path +
                    self.server.web.authentication_file_name)
                authentication_file = FileHandler(location=file_path)
                if authentication_file:
                    return(
                        self.headers.get('authorization') ==
                        'Basic %s' % self._get_login_data(
                            authentication_file))
                if self._authentication_location == self.server.web.root:
                    break
                self._authentication_location = FileHandler(
                    location=self._authentication_location.directory_path)
# # python3.4
# #             login_data_match = re.compile(
# #                 '(?P<name>[^:]+):(?P<password>.+)$'
# #             ).match(base64_decode(
# #                 self.headers.get('authorization', '')[builtins.len(
# #                     'Basic '
# #                 ):]
# #             ).decode(self.server.web.encoding))
            login_data_match = re.compile(
                '(?P<name>[^:]+):(?P<password>.+)$'
            ).match(base64_decode(self.headers.get(
                'authorization', ''
            )[builtins.len('Basic '):]))
# #
            login_data = None
            if login_data_match:
                login_data = {
                    'name': login_data_match.group('name'),
                    'password': login_data_match.group('password')}
            return builtins.bool(
                self.server.web.authentication_handler is None or
                self.server.web.authentication_handler(login_data, self))
        return True

    @JointPoint
# # python3.4     def _is_valid_reference(self: Self) -> builtins.bool:
    def _is_valid_reference(self):
        '''
            Checks weather the requested is one of a python module-, static- \
            or dynamic file request. Returns "True" if so and "False" \
            otherwise.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)

            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + '_is_valid_reference')
            >>> handler.path = handler.requested_file.name
            >>> handler._is_valid_reference()
            False

            >>> handler.requested_file.make_directory()
            True
            >>> handler._is_valid_reference()
            True

            >>> handler.requested_file = FileHandler(
            ...     handler.requested_file.path +
            ...     handler.server.web.authentication_file_name)
            >>> handler.requested_file.content = 'hans:hans'
            >>> handler._is_valid_reference()
            False

            >>> handler.requested_file = None
            >>> handler.server.web.module_loading = True
            >>> handler.path = 'doctest'
            >>> handler._is_valid_reference()
            True
        '''
        if((self.server.web.module_loading is True or
            self.server.web.module_loading == self.path) and (
            (self.path == '__main__' and __name__ != '__main__') or
            Module.get_file_path(context_path=self.path))
           ):
            self.load_module = True
            return True
        elif self.requested_file:
            if self._is_valid_requested_file():
                return True
        return False

    @JointPoint
# # python3.4     def _is_valid_requested_file(self: Self) -> builtins.bool:
    def _is_valid_requested_file(self):
        '''Determines if the current requested file points to a valid file.'''
        patterns = self.server.web.dynamic_mime_type_pattern + \
            self.server.web.static_mime_type_pattern
        return(
            self.requested_file.is_file() and self.requested_file.name !=
            self.server.web.authentication_file_name and self._check_pattern(
                patterns=patterns, subject=self.requested_file.mime_type
            ) is not False or self.server.web.directory_listing and
            self.requested_file.is_directory())

    @JointPoint
# # python3.4     def _is_dynamic(self: Self) -> builtins.bool:
    def _is_dynamic(self):
        '''
            Determines if the current request points to a dynamic executable \
            file or is a static type which should be send back unmodified.
        '''
        return builtins.bool(self.load_module or self._check_pattern(
            self.server.web.dynamic_mime_type_pattern,
            self.requested_file.mime_type))

        # # endregion

    @JointPoint
# # python3.4
# #     def _do_data_request(self: Self, type: builtins.str) -> Self:
    def _do_data_request(self, type):
# #
        '''Is triggered if a special request is coming.'''
        self.request_type = type[builtins.len('do_'):].lower()
# # python3.4
# #         self.data_type, post_data = cgi.parse_header(
# #             self.headers.get_content_type())
        self.data_type, post_data = cgi.parse_header(
            self.headers.gettype())
# #
        content_length = builtins.int(self.headers.get('content-length', 0))
        if not __test_mode__:
            if self.data_type == 'application/x-www-form-urlencoded':
# # python3.4
# #                 self.data = urlparse.parse_qs(self.rfile.read(
# #                     content_length
# #                 ).decode(self.server.web.encoding))
                self.data = cgi.parse_qs(
                    self.rfile.read(content_length),
                    keep_blank_values=True)
# #
                for name, value in self.data.items():
                    if Object(content=value).is_binary():
                        self.data[name] = {'content': value}
            elif self.data_type == 'multipart/form-data':
                self.data = self._determine_data()
            elif self.data_type == 'application/json':
# # python3.4
# #                 self.data = json.loads(self.rfile.read(
# #                     content_length
# #                 ).decode(self.server.web.encoding))
                self.data = json.loads(
                    self.rfile.read(content_length),
                    encoding=self.server.web.encoding)
# #
            else:
                self.data = {
                    'type': self.data_type,
                    'content': self.rfile.read(content_length)}
        return self.do_GET()

    @JointPoint
# # python3.4
# #     def _get_login_data(
# #         self: Self, authentication_file: FileHandler
# #     ) -> builtins.str:
    def _get_login_data(self, authentication_file):
# #
        '''Determines needed login data for current request.'''
        __logger__.info(
            'Use authentication file "%s".', authentication_file._path)
# # python3.4
# #         match = re.compile(
# #             self.server.web.authentication_file_content_pattern
# #         ).fullmatch(authentication_file.content.strip())
# #         return base64_encode(('%s:%s' % (
# #             match.group('name'), match.group('password')
# #         )).encode(self.server.web.encoding)).decode(
# #             self.server.web.encoding)
        match = re.compile(
            '(?:%s)$' % self.server.web.authentication_file_content_pattern
        ).match(authentication_file.content.strip())
        return base64_encode(
            '%s:%s' % (match.group('name'), match.group('password')))
# #

    @JointPoint
# # python3.4     def _determine_data(self: Self) -> builtins.dict:
    def _determine_data(self):
        '''
            Determines the post values given by an html form. File uploads \
            are includes as bytes.
        '''
# # python3.4
# #         form = cgi.FieldStorage(
# #             fp=self.rfile, headers=self.headers, keep_blank_values=True,
# #             strict_parsing=True,
# #             environ=self._determine_environment_variables(),
# #             encoding=self.server.web.encoding)
        form = cgi.FieldStorage(
            fp=self.rfile, headers=self.headers, keep_blank_values=True,
            strict_parsing=True,
            environ=self._determine_environment_variables())
# #
        data = {}
        for name in form:
            data[name] = []
            if builtins.hasattr(form[name], 'file') and form[name].filename:
                data[name].append(form[name])
            elif builtins.isinstance(form[name], builtins.list):
                for value in form[name]:
                    if builtins.hasattr(value, 'file') and value.filename:
                        data[name].append(value)
                    else:
                        data[name].append(value.value)
            else:
                data[name].append(form[name].value)
        return data

    @JointPoint
# # python3.4
# #     def _determine_environment_variables(self: Self) -> os._Environ:
    def _determine_environment_variables(self):
# #
        '''
            Determines all needed environment variables needed to determine \
            given post data with cgi module.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('content-type: text/plain'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('content-type', 'text/plain')
            >>> # #
            >>> handler.command = ''

            >>> dict(
            ...     handler._determine_environment_variables()
            ... ) # doctest: +ELLIPSIS
            {'...': '...'}

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String(
            ...             'accept: text/plain\\nContent-Type: text/plain'
            ...         ), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('accept', 'text/plain')
            >>> # #
            >>> dict(
            ...     handler._determine_environment_variables()
            ... ) # doctest: +ELLIPSIS
            {'...': '...'}

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('cookie: hans=peter'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('cookie', 'hans=peter')
            >>> # #
            >>> dict(
            ...     handler._determine_environment_variables()
            ... ) # doctest: +ELLIPSIS
            {'...': '...'}
        '''
        accept = []
        if 'accept' in self.headers:
            for line in self.headers['accept'].split('\n'):
                accept += line.split(',')
        variables = deepcopy(os.environ)
# # python3.4
# #         content_type = self.headers.get_content_type()
        content_type = self.headers.get('content-type', 'text/plain')
# #
        variables.update({
            'HTTP_ACCEPT': ','.join(accept),
            'REQUEST_METHOD': self.command,
            'CONTENT_TYPE': content_type,
            'QUERY_STRING': self.parameter,
            'REMOTE_HOST': self.host,
            'CONTENT_LENGTH': builtins.str(self.headers.get(
                'content-length', 0)),
            'HTTP_USER_AGENT': '',
            'HTTP_COOKIE': '',
            'HTTP_REFERER': ''})
        for variable_name in variables:
# # python3.4
# #             if variable_name.replace('_', '-').lower() in self.headers:
# #                 variables[variable_name] = self.headers.get(
# #                     variable_name.replace('_', '-').lower())
# #         cookie_content = ', '.join(builtins.filter(
# #             None, self.headers.get_all('cookie', [])))
# #         if cookie_content:
# #             variables['HTTP_COOKIE'] = cookie_content
            if self.headers.get(
                variable_name.replace('_', '-').lower(), False
            ):
                variables[variable_name] = self.headers.get(
                    variable_name.replace('_', '-').lower())
# #
        return variables

    @JointPoint
# # python3.4
# #     def _send_no_authorization_error(self: Self) -> Self:
    def _send_no_authorization_error(self):
# #
        '''This method is called if authentication failed.'''
        self.send_response(401)
        message = 'You request a protected location'
# # python3.4
# #         if 'authorization' in self.headers:
        if self.headers.get('authorization', False):
# #
            message = 'Requested authentication failed'
        if not __test_mode__:
            self.send_header(
                'WWW-Authenticate', 'Basic realm=\"%s\"' % message)
            self.send_header(
                'Content-Type',
                'text/html; charset=%s' % self.server.web.encoding)
        self.end_headers()
        return self

    @JointPoint
# # python3.4
# #     def _send_no_file_error(
# #         self: Self, valid_request=True, debug=False
# #     ) -> Self:
    def _send_no_file_error(self, valid_request=True, debug=False):
# #
        '''
            Generates a http-404-error if no useful file was found for \
            responding.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)

            >>> handler.path = '/'
            >>> handler.requested_file = __test_folder__
            >>> handler._send_no_file_error(debug=True) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.server.web.module_loading = ''
            >>> handler._send_no_file_error(debug=True) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.server.web.module_loading = True
            >>> handler._send_no_file_error(debug=True) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.path = ''
            >>> handler._send_no_file_error(debug=True) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + '_send_no_file_error')
            >>> handler.requested_file.content = ''
            >>> handler._send_no_file_error(
            ...     False, debug=True
            ... ) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        error_message = 'Requested file not found'
        if __logger__.isEnabledFor(logging.DEBUG) or sys.flags.debug or debug:
            error_message = (
                'Eather none of the following default module names "%s" nor '
                'none of the following default file name pattern "%s" found' %
                ('", "'.join(self.server.web.default_module_names),
                 '", "'.join(self.server.web.default_file_name_pattern)))
            if builtins.isinstance(
                self.server.web.module_loading, builtins.str
            ):
                error_message = (
                    'Eather default module name "%s" nor none of the following'
                    ' default file name pattern "%s" found' % (
                        self.server.web.module_loading, '", "'.join(
                            self.server.web.default_file_name_pattern)))
            elif not self.server.web.module_loading:
                error_message = (
                    'None of the following default file name pattern "%s" '
                    'found' % '", "'.join(
                        self.server.web.default_file_name_pattern))
            if self.path:
                error_message = ('No accessible file "%s" found' % FileHandler(
                    location=self.server.web.root.path + self.path
                )._path)
            if not valid_request:
                error_message = (
                    "Given request isn't valid. Check your white- and "
                    'blacklists')
            if self.requested_file.is_file():
                error_message += \
                    '. Detected mime-type "%s"' % self.requested_file.mime_type
        self.send_error(404, re.compile('\n+').sub('\n', error_message))
        return self

    @JointPoint
# # python3.4
# #     def _check_pattern(
# #         self: Self, patterns: Iterable, subject: builtins.str
# #     ) -> (builtins.str, builtins.bool):
    def _check_pattern(self, patterns, subject):
# #
        '''
            Checks if one of a list of given regular expression patterns \
            matches the given subject.
        '''
        for pattern in patterns:
# # python3.4             if re.compile(pattern).fullmatch(subject):
            if re.compile('(?:%s)$' % pattern).match(subject):
                return subject
        return False

    @JointPoint
# # python3.4     def _is_valid_request(self: Self) -> builtins.bool:
    def _is_valid_request(self):
        '''Checks if given request fulfills all restrictions.'''
        return self._request_in_pattern_list(
            self.server.web.request_whitelist
        ) and not self._request_in_pattern_list(
            self.server.web.request_blacklist)

    @JointPoint
# # python3.4
# #     def _request_in_pattern_list(
# #         self: Self, pattern_list: Iterable
# #     ) -> builtins.bool:
    def _request_in_pattern_list(self, pattern_list):
# #
        '''Checks if current request matches on of the given pattern.'''
# # python3.4
# #         patterns = re.compile('(?P<request_type>.+?):(?P<request_uri>.*)')
        patterns = re.compile(
            '^(?P<request_type>.+?):(?P<request_uri>.*)$')
# #
        request_type_uppercase = self.external_request_type.upper()
        for pattern in pattern_list:
# # python3.4             match = patterns.fullmatch(pattern)
            match = patterns.match(pattern)
            request_types = match.group('request_type').split('|')
# # python3.4
# #             if(request_type_uppercase in request_types or
# #                '*' in request_types
# #                ) and re.compile(match.group('request_uri')).fullmatch(
# #                    self.external_request_uri) is not None:
            if(request_type_uppercase in request_types or
               '*' in request_types
               ) and re.compile('(?:%s)$' % match.group(
                   'request_uri'
               )).match(self.external_request_uri) is not None:
# #
                return True
        return False

    @JointPoint
# # python3.4     def _determine_host(self: Self) -> Self:
    def _determine_host(self):
        '''
            Determines the full host name with port included (if it's not \
            "80").

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> handler.server.web.host_name = 'test'
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.server.web.port = 80
            >>> handler._determine_host() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> handler.host
            'test'

            >>> handler.server.web.port = 8080
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('accept: text/plain'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('accept', 'text/plain')
            >>> # #
            >>> handler._determine_host() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> handler.host
            'test:8080'

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('x-forwarded-host: hans\\nHost: hans'),
            ...         seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('x-forwarded-host', 'hans')
            ...     handler.headers.add_header('host', 'hans')
            >>> # #
            >>> handler._determine_host() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> handler.host
            'hans'

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('Host: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('host', 'hans')
            >>> # #
            >>> handler._determine_host() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> handler.host
            'hans'
        '''
        self.host = self.server.web.host_name
        if self.server.web.port != 80:
            self.host += ':%d' % self.server.web.port
# # python3.4
# #         if 'x-forwarded-host' in self.headers:
# #             self.host = self.headers.get('x-forwarded-host')
# #         elif 'host' in self.headers:
# #             self.host = self.headers.get('host')
        if self.headers.get('x-forwarded-host', False):
            self.host = self.headers.get('x-forwarded-host')
        elif self.headers.get('host', False):
            self.host = self.headers.get('host')
# #
        return self

    @JointPoint
# # python3.4
# #     def _handle_redirect(self: Self, external=True) -> builtins.bool:
    def _handle_redirect(self, external=True):
# #
        '''
            Deals with specified redirects. External Redirects will send an \
            http redirection code.
        '''
# # python3.4
# #         patterns = re.compile('(?P<request_type>.+?):(?P<request_uri>.*)')
        patterns = re.compile('(?P<request_type>.+?):(?P<request_uri>.*)$')
# #
        request_type_uppercase = self.request_type.upper()
        redirects = self.server.web.internal_redirects
        if external:
            redirects = self.server.web.external_redirects
        for source, target in redirects:
# # python3.4             source_match = patterns.fullmatch(source)
            source_match = patterns.match(source)
            request_types = source_match.group('request_type').split('|')
# # python3.4
# #             pattern = re.compile(source_match.group('request_uri'))
# #             if(request_type_uppercase in request_types or
# #                '*' in request_types
# #                ) and pattern.fullmatch(
# #                    self.external_request_uri) is not None:
            pattern = re.compile('(?:%s)$' % source_match.group(
                'request_uri'))
            if(request_type_uppercase in request_types or
               '*' in request_types
               ) and pattern.match(self.external_request_uri) is not None:
# #
                self._handle_matched_redirect(
                    pattern, patterns, target, external)
                return True
        return False

    @JointPoint
# # python3.4
# #     def _handle_matched_redirect(
# #         self: Self, pattern: builtins.type(re.compile('')),
# #         patterns: builtins.type(re.compile('')), target: builtins.str,
# #         external: builtins.bool
# #     ) -> Self:
    def _handle_matched_redirect(
        self, pattern, patterns, target, external
    ):
# #
        '''Performs an internal or external redirect.'''
        if external:
            if not __test_mode__:
                self.external_request_uri = pattern.sub(
                    target, self.external_request_uri)
                self.send_response(301).send_header(
                    'Location', self.external_request_uri)
                self.end_headers()
        else:
            target_match = patterns.match(target)
            if target_match.group('request_type') != '-':
                self.request_type = target_match.group('request_type')
            for request in target_match.group('request_uri').split('#'):
                self.request_uri = pattern.sub(
                    request, self.external_request_uri
                ).format(host_name=re.compile(':[0-9]+$').sub(
                    '', self.host))
                if FileHandler(location=self.request_uri):
                    break
        return self

    @JointPoint
# # python3.4
# #     def _create_environment_variables(self: Self) -> builtins.str:
    def _create_environment_variables(self):
# #
        '''Creates all request specified environment-variables.'''
        self._determine_host().request_uri = self.external_request_uri = \
            self.path
        self._handle_redirect(external=False)
# # python3.4
# #         match = re.compile(
# #             '[^/]*/+(?P<path>.*?)(?:{delimiter}(?P<parameter>.*))?'.format(
# #                 delimiter=self.server.web.request_parameter_delimiter)
# #         ).fullmatch(self.request_uri)
        match = re.compile(
            '[^/]*/+(?P<path>.*?)'
            '(?:{delimiter}(?P<parameter>.*))?$'.format(
                delimiter=self.server.web.request_parameter_delimiter)
        ).match(self.request_uri)
# #
        self.path = ''
        if match:
# # python3.4
# #             self.path = posixpath.normpath(urlparse.unquote(match.group(
# #                 'path')))
            self.path = posixpath.normpath(urllib.unquote(match.group(
                'path')))
# #
            if self.path == '.':
                self.path = ''
            self.parameter = match.group('parameter')
        self.requested_file = FileHandler(
            location=self.server.web.root.path + self.path)
        self._authentication_location = self.server.web.root
        if self.requested_file:
            self._authentication_location = self.requested_file
            if self.requested_file.is_file():
                self._authentication_location = FileHandler(
                    location=self.requested_file.directory_path)
        cookie_handler = self.get_cookie()
        if cookie_handler is not None:
            for key, morsel in cookie_handler.items():
                self.cookie[key] = morsel.value
        self.get = self.parse_url(self.request_uri)[1]
        return self.path

    @JointPoint
# # python3.4
# #     def _set_dynamic_or_static_get(
# #         self: Self, file_name: builtins.str
# #     ) -> Self:
    def _set_dynamic_or_static_get(self, file_name):
# #
        '''
            Makes a dynamic or static respond depending on incoming request.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler.load_module = True
            >>> handler._set_dynamic_or_static_get('test') # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        self.requested_file_name = file_name
        if self._is_dynamic():
            return self._dynamic_get()
        return self._static_get()

    @JointPoint
# # python3.4     def _default_get(self: Self) -> builtins.bool:
    def _default_get(self):
        '''
            Handles every request which doesn't takes a file or python module \
            with.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('cookie: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('cookie', 'hans')
            >>> # #

            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + 'index.py')
            >>> handler.requested_file.content = ''
            >>> handler._default_get()
            True

            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('cookie: hans=peter'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('cookie', 'hans=peter')
            >>> # #

            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + 'index.py')
            >>> handler.requested_file.content = ''
            >>> handler._default_get()
            True

            >>> handler.server.web.directory_listing = False
            >>> handler.requested_file.remove_file()
            True
            >>> handler._default_get()
            False

            >>> handler.server.web.module_loading = True
            >>> handler.server.web.default = 'doctest'
            >>> handler._default_get()
            True

            >>> handler.server.web.default = ''
            >>> handler.server.web.default_module_names = 'doctest',
            >>> handler.data['__no_respond__'] = True
            >>> handler.respond = False
            >>> handler._default_get()
            True
        '''
        if self.server.web.default:
            self._handle_given_default_get()
            return True
        if(self.server.web.module_loading and
           self._is_default_module_requested()):
            return True
        for file in self.server.web.root:
            if self._check_pattern(
                self.server.web.default_file_name_pattern, file.name
            ):
                self.requested_file = file
                self._set_dynamic_or_static_get(file_name=file.name)
                return True
        if self.server.web.directory_listing:
            self._static_get()
            return True
        return False

    @JointPoint
# # python3.4
# #     def _is_default_module_requested(self: Self) -> builtins.bool:
    def _is_default_module_requested(self):
# #
        '''
            Handle a default module request if possible.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler._is_default_module_requested()
            False

            >>> handler.server.web = Web(
            ...     __test_folder__, module_loading='doctest')
            >>> handler._is_default_module_requested()
            True
        '''
        if self.server.web.module_loading:
# # python3.4
# #             if builtins.isinstance(
# #                 self.server.web.module_loading, builtins.str
# #             ) and self._handle_default_modules_get(
# #                 self.server.web.module_loading
# #             ):
            if builtins.isinstance(self.server.web.module_loading, (
                builtins.unicode, builtins.str
            )) and self._handle_default_modules_get(
                self.server.web.module_loading
            ):
# #
                return True
            for module_name in self.server.web.default_module_names:
                if self._handle_default_modules_get(module_name):
                    return True
        return False

    @JointPoint
# # python3.4
# #     def _handle_default_modules_get(
# #         self: Self, module_name: builtins.str
# #     ) -> (Self, builtins.bool):
    def _handle_default_modules_get(self, module_name):
# #
        '''
            Handles requests which wants the current defaults modules \
            (initially called module) run for a server thread.

            Examples:

            >>> test_globals_backup = __test_globals__['__name__']

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('test: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('test', 'hans')
            >>> # #

            >>> handler._handle_default_modules_get('not_existing')
            False

            >>> handler._handle_default_modules_get('__main__')
            False

            >>> __test_globals__['__name__'] = __module_name__
            >>> handler._handle_default_modules_get(
            ...     '__main__'
            ... ) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and param...

            >>> __test_globals__['__name__'] = test_globals_backup
        '''
        if module_name == '__main__':
            if __name__ != '__main__':
                self.load_module = True
                return self._set_dynamic_or_static_get(file_name=module_name)
        elif Module.get_file_path(context_path=module_name):
            self.load_module = True
            return self._set_dynamic_or_static_get(file_name=module_name)
        return False

    @JointPoint
# # python3.4     def _handle_given_default_get(self: Self) -> Self:
    def _handle_given_default_get(self):
        '''
            Handles request with no explicit file or module to run.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> handler.path = '/'
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String('cookie: hans'), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header('cookie', 'hans')
            >>> # #

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> handler._handle_given_default_get() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...Determine "" as default file...'

            >>> handler.server.web.module_loading = True
            >>> handler.server.web.default = 'doctest'
            >>> handler._handle_given_default_get() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...Determine "doctest" as default module...'
        '''
        if((self.server.web.module_loading is True or
            self.server.web.module_loading == self.server.web.default) and
           Module.get_file_path(context_path=self.server.web.default)):
            self.load_module = True
            __logger__.info(
                'Determine "%s" as default module.', self.server.web.default)
        self.requested_file = FileHandler(
            location=self.server.web.root.path + self.server.web.default)
        if self.requested_file:
            __logger__.info(
                'Determine "%s" as default file.', self.server.web.default)
        return self._set_dynamic_or_static_get(
            file_name=self.server.web.default)

    @JointPoint
# # python3.4     def _static_get(self: Self) -> Self:
    def _static_get(self):
        '''
            Handles a static file-request.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + '_static_get')
            >>> handler.requested_file.content = ''
            >>> # # python2.7
            >>> if sys.version_info.major < 3:
            ...     handler.headers = handler.MessageClass(
            ...         String(
            ...             'if-modified-since: %s' % handler.date_time_string(
            ...                 int(handler.requested_file.timestamp))
            ...         ), seekable=False)
            ... else:
            ...     handler.headers = handler.MessageClass()
            ...     handler.headers.add_header(
            ...         'if-modified-since', handler.date_time_string(
            ...             int(handler.requested_file.timestamp)))
            >>> # #

            >>> handler._static_get() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        if not __test_mode__ and self.requested_file.is_directory():
            if self.data_type == 'multipart/form-data':
                self._save_uploaded_files()
            '''
                If a directory was requested and no trailing slash where \
                given a 301 redirect will be returned to same request with \
                trailing slash.
            '''
            if not re.compile(
                '/(%s.*)?$' % self.server.web.request_parameter_delimiter
            ).search(self.external_request_uri):
                self.send_response(301).send_header('Location', re.compile(
                    '((%s.*)?)$' % self.server.web.request_parameter_delimiter
                ).sub('/\\1', self.external_request_uri))
                return self.end_headers()
            return self.list_directory()
        try:
            file_handler = builtins.open(self.requested_file._path, mode='rb')
        except builtins.IOError:
            self._send_no_file_error()
            return self
# # python3.4
# #         if(self.headers.get('if-modified-since') ==
# #            self.date_time_string(
# #                builtins.int(self.requested_file.timestamp))):
        if(self.headers.get('if-modified-since') ==
           self.date_time_string(
               builtins.int(self.requested_file.timestamp))):
# #
            return self._send_not_modified_header()
        return self._send_static_file(output=file_handler)

    @JointPoint
# # python3.4     def _save_uploaded_files(self: Self) -> Self:
    def _save_uploaded_files(self):
        '''
            Uploaded data to a directory are saved automatically by this \
            method.
        '''
        for items in self.data.values():
            for item in items:
# # python3.4
# #                 if(builtins.len(item) == 4 and
# #                    'content' in item and 'name' in item and
# #                    'disposition' in item and 'disposition' in item and
# #                    'encoding' in item):
# #                     FileHandler(
# #                         self.requested_file.path + item['name'],
# #                         encoding=item['encoding']
# #                     ).set_content(content=item['content'], mode='w+b')
                if(builtins.len(item) == 3 and
                   'content' in item and 'name' in item and
                   'disposition' in item):
                    FileHandler(
                        self.requested_file.path + item['name']
                    ).set_content(content=item['content'], mode='w+b')
# #
        return self

    @JointPoint
# # python3.4
# #     def _send_static_file(
# #         self: Self, output: (builtins.str, _io.BufferedReader)
# #     ) -> Self:
    def _send_static_file(self, output):
# #
        '''
            Sends given output to client.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + '_static_get')
            >>> handler.requested_file.content = ''
            >>> handler.server.web.file_size_stream_threshold_in_byte = 0

            >>> handler._send_static_file('') # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        threshold = self.server.web.file_size_stream_threshold_in_byte
        if threshold < self.requested_file.size:
            self.send_content_type_header(mime_type='application/octet-stream')
            self.send_header('Content-Transfer-Encoding', 'binary')
        else:
            self.send_content_type_header(
                mime_type=self.requested_file.get_mime_type(web=True))
        self.send_static_file_cache_header(
            timestamp=self.requested_file.timestamp)
        self.send_content_length_header(
            size=builtins.int(self.requested_file.size))
        self.end_headers()
        return self._send_output(output)

    @JointPoint
# # python3.4     def _send_not_modified_header(self: Self) -> Self:
    def _send_not_modified_header(self):
        '''Sends a header to client indicating cached file hasn't changed.'''
        self.send_content_type_header(
            mime_type=self.requested_file.mime_type, response_code=304
        ).send_static_file_cache_header(
            timestamp=self.requested_file.timestamp
        ).send_content_length_header(
            size=builtins.int(self.requested_file.size))
        self.end_headers()
        return self

    @JointPoint
# # python3.4
# #     def _send_output(
# #         self: Self, output: (builtins.str, _io.BufferedReader)
# #     ) -> Self:
    def _send_output(self, output):
# #
        '''Sends the final given output to client.'''
        if not (__test_mode__ or self.request_type == 'head'):
            if self._encoded_output:
                self.wfile.write(self._encoded_output)
# # python3.4
# #             elif builtins.isinstance(output, builtins.bytes):
            elif builtins.isinstance(output, (
                builtins.unicode, builtins.str
            )):
# #
                self.wfile.write(output)
            elif builtins.isinstance(output, builtins.str):
                self.wfile.write(output.encode(self.server.web.encoding))
            else:
                self.copyfile(output, self.wfile)
                output.close()
        return self

    @JointPoint
# # python3.4
# #     def _gzip(
# #         self: Self, content: (builtins.str, builtins.bytes)
# #     ) -> builtins.bytes:
    def _gzip(self, content):
# #
        '''
            Compresses the given content and returns the encoded result.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)

            >>> isinstance(handler._gzip(''), bytes)
            True

            >>> isinstance(handler._gzip(bytes()), bytes)
            True
        '''
# # python3.4         output = io.BytesIO()
        output = StringIO.StringIO()
        gzip_file_handler = gzip.GzipFile(
            fileobj=output, mode='w', compresslevel=5)
# # python3.4
# #         if builtins.isinstance(content, builtins.bytes):
# #             gzip_file_handler.write(content)
# #         else:
# #             gzip_file_handler.write(content.encode(
# #                 encoding=self.server.web.encoding))
        gzip_file_handler.write(content.encode(self.server.web.encoding))
# #
        gzip_file_handler.close()
        return output.getvalue()

    @JointPoint
# # python3.4     def _dynamic_get(self: Self) -> Self:
    def _dynamic_get(self):
        '''
            Handles a dynamic file or python module request. It initializes \
            the given script-file or python module environment weather to \
            decide running it in its own thread or not. If no respond is \
            expected from client it could be run without its own thread \
            environment.
        '''
        self.request_arguments = (
            ('requested_file_name', self.requested_file_name),
            ('host', self.host), ('request_uri', self.request_uri),
            ('external_request_uri', self.external_request_uri),
            ('get', self.get), ('data', self.data), ('cookie', self.cookie),
            ('request_type', self.request_type),
            ('external_request_type', self.external_request_type),
            ('shared_data', self.server.web.shared_data), ('handler', self))
        if '__no_respond__' not in self.data:
            self.respond = True
            return self._run_request()
        self.__class__.last_running_worker = threading.Thread(
            target=self._run_request)
        self.__class__.last_running_worker.start()
        return self

    @JointPoint
# # python3.4     def _run_request(self: Self) -> Self:
    def _run_request(self):
        '''
            Decides to run the given script as python-module or standalone \
            script-file.
        '''
        if self.load_module:
            return self._run_requested_module()
        return self._run_requested_file()

    @JointPoint
# # python3.4     def _run_requested_file(self: Self, debug=False) -> Self:
    def _run_requested_file(self, debug=False):
        '''
            Runs a given external process in a subprocess. Output and errors \
            are piped to requested client.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)
            >>> handler.requested_file = FileHandler(
            ...     __test_folder__.path + '_run_requested_file')
            >>> handler.requested_file.content = ''
            >>> handler.request_arguments = ('hans', 'peter'),

            >>> handler.respond = False
            >>> handler._run_requested_file() # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...

            >>> handler.request_arguments = ('hans', 'peter'),
            >>> handler._run_requested_file(True) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
        '''
        self.request_arguments = builtins.list(builtins.map(
            lambda element: builtins.str(element[1]), self.request_arguments))
        self.request_arguments[0] = self.server.web.root.path + \
            self.request_arguments[0][1]
        __logger__.debug('Execute file "%s".', self.request_arguments[0])
        self.server.web.number_of_running_threads += 1
        try:
            output, errors = subprocess.Popen(
                self.request_arguments, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
        except builtins.OSError as exception:
            output = ''
            errors = '%s: %s' % (
                exception.__class__.__name__, builtins.str(exception))
        self.server.web.number_of_running_threads -= 1
        size = builtins.len(output)
# # python3.4
# #         if not builtins.isinstance(errors, builtins.str):
        if not builtins.isinstance(errors, (
            builtins.unicode, builtins.str
        )):
# #
            errors = errors.decode(
                encoding=self.server.web.encoding, errors='strict')
        if self.respond:
            if errors:
                program_description = ''
                if(sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG) or
                   debug):
                    program_description = ' "%s"' % self.request_arguments[0]
                self.send_error(
                    500, 'Internal server error with cgi program%s: "%s"' %
                    (program_description, re.compile('\n+').sub('\n', errors)))
            else:
                '''Check if given output contains a header.'''
                header_match = re.compile(
                    '[A-Z0-9]+/([0-9]+\.)+[0-9]+ [0-9]{3} [a-zA-Z ]+\n'
                    '([^:]+: .+\n)+\n.+'
                ).match(output.decode(encoding=self.server.web.encoding))
                if not header_match:
                    self.send_content_type_header().send_content_length_header(
                        size, dynamic_output=output
                    ).end_headers()
                self._send_output(output)
        if errors:
            __logger__.critical(
                'Error in common gateway interface program "%s": %s',
                self.request_arguments[0], errors)
        return self

    @JointPoint
# # python3.4     def _run_requested_module(self: Self) -> Self:
    def _run_requested_module(self):
        '''
            Imports and runs a given python module. Errors and output are \
            piped to requested client.
        '''
        self.request_arguments = builtins.dict(self.request_arguments)
        '''Redirect output buffer.'''
        print_default_buffer_backup = Print.default_buffer
        Print.default_buffer = self.server.web.thread_buffer
# # python3.4         sys_path_backup = sys.path.copy()
        sys_path_backup = copy(sys.path)
        sys.path = [self.server.web.root.path] + sys.path
        self.server.web.number_of_running_threads += 1
        requested_module = builtins.__import__(
            self.request_arguments['requested_file_name'])
        '''Extend requested scope with request dependent globals.'''
        requested_module.__request_arguments__ = self.request_arguments
        sys.path = sys_path_backup
        __logger__.debug('Run module "%s".', requested_module)
        return self._handle_module_running(
            requested_module, print_default_buffer_backup, sys_path_backup)

    @JointPoint
# # python3.4
# #     def _handle_module_running(
# #         self: Self, requested_module: types.ModuleType,
# #         print_default_buffer_backup: builtins.object,
# #         sys_path_backup: Iterable
# #     ) -> Self:
    def _handle_module_running(
        self, requested_module, print_default_buffer_backup,
        sys_path_backup
    ):
# #
        '''Handles exceptions raising in requested modules.'''
        try:
            if not __test_mode__:
                Module.determine_caller(
                    callable_objects=Module.get_defined_callables(
                        scope=requested_module)
                )[1]()
        except builtins.BaseException as exception:
            self._handle_module_exception(requested_module, exception)
        else:
            if self.respond:
                self.send_content_type_header().send_content_length_header(
                    size=builtins.len(self.server.web.thread_buffer.content),
                    dynamic_output=self.server.web.thread_buffer.content
                ).end_headers()
        finally:
            self.server.web.number_of_running_threads -= 1
            if self.respond:
                self._send_output(
                    output=self.server.web.thread_buffer.clear())
            Print.default_buffer = print_default_buffer_backup
        return self

    @JointPoint
# # python3.4
# #     def _handle_module_exception(
# #         self: Self, requested_module: types.ModuleType,
# #         exception: builtins.BaseException, debug=False
# #     ) -> Self:
    def _handle_module_exception(
        self, requested_module, exception, debug=False
    ):
# #
        '''
            This method handles each exception raised by running a module \
            which was requested by client.

            Examples:

            >>> handler = CGIHTTPRequestHandler()
            >>> handler.server = Class()
            >>> handler.server.web = Web(__test_folder__)

            >>> try:
            ...     raise OSError('hans')
            ... except OSError as exception:
            ...     handler._handle_module_exception(
            ...         __import__('doctest'), exception, True)
            Traceback (most recent call last):
            ...
            OSError: hans

            >>> handler.respond = True
            >>> try:
            ...     raise OSError('hans')
            ... except BaseException as exception:
            ...     handler._handle_module_exception(
            ...         __import__('doctest'), exception, True)
            Traceback (most recent call last):
            ...
            OSError: hans

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> try:
            ...     raise OSError('hans')
            ... except BaseException as exception:
            ...     handler._handle_module_exception(
            ...         __import__('doctest'), exception
            ...     ) # doctest: +ELLIPSIS
            Object of "CGIHTTPRequestHandler" with request uri "" and parame...
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '... - CRITICAL - Error in module "doctest" OSError: hans...'
        '''
        if self.respond:
            if(sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG) or
               debug):
# # python3.4
# #                 self.send_error(
# #                     500, '%s: %s' %
# #                     (exception.__class__.__name__,
# #                      re.compile('\n+').sub('\n', builtins.str(exception))))
                self.send_error(
                    500, '%s: %s' %
                    (exception.__class__.__name__,
                     re.compile('\n+').sub('\n', builtins.unicode(
                         builtins.str(exception), boostNode.ENCODING))))
# #
            else:
                self.send_error(500, 'Internal server error')
        if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG) or debug:
            raise
        else:
            __logger__.critical(
                'Error in module "%s" %s: %s', requested_module.__name__,
                exception.__class__.__name__, builtins.str(exception))
        return self

        # endregion

    # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what \
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = __test_buffer__ = __test_folder__ = __test_globals__ = None
'''
    Extends this module with some magic environment variables to provide \
    better introspection support. A generic command line interface for some \
    code preprocessing tools is provided by default.
'''
Module.default(
    name=__name__, frame=inspect.currentframe(), default_caller=Web.__name__)

# endregion

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion
