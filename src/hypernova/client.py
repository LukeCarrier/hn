#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Client application package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import argparse
import configparser
from http.client import HTTPConnection
from hypernova import GPG
from hypernova.libraries.configuration import ConfigurationFactory, LoadError
import json
import os
import sys

class Client:

    addr = None
    port = None

    connection = None

    M_GET  = 'GET'
    M_POST = 'POST'

    def __init__(self, addr='127.0.0.1', port=8080):

        self.addr = addr
        self.port = port

        self._init_connection()
        self._init_gpg()

    def _init_connection(self):

        self._connection = HTTPConnection(self.addr, self.port)

    def _init_gpg(self):

        self._gpg = GPG.get_gpg(gnupghome=os.path.join(os.getenv('HOME'),
                                                       '.gnupg'))

    def query(self, params, client_fp, server_fp):

        if not isinstance(params, str):
            params = json.dumps(params)

        params = self._gpg.encrypt(params, server_fp, sign=client_fp)
        encrypted_params = str(params)

        if not params:
            raise ValueError('Invalid passphrase, or the server\'s key has ' \
                             'not been signed')

        http_headers = {'Content-Length': len(encrypted_params)}
        self._connection.request(self.M_GET, '/', body=encrypted_params,
                                 headers=http_headers)

        response = self._connection.getresponse()
        response_data = str(response.read(), 'UTF-8')

        response_data = self._gpg.decrypt(response_data)
        if response_data.fingerprint != server_fp:
            raise ValueError('Response was not signed')

        self._connection.close()

        return json.loads(str(response_data))


class ClientActionBase:
    """
    Base class for all actions within the client.
    """

    _arg_parsers = {}
    _args        = None

    _config = None

    def __init__(self, cli_args, config_dir):
        """
        Run the action.
        """

        self._args = cli_args

        self._config_dir = config_dir
        self._config     = ConfigurationFactory.get('hypernova')

    def init_subparser(subparser):
        """
        Prepare subparsers for subactions/parameters.
        """

        return subparser


class ClientConfigAction(ClientActionBase):
    """
    Configuration management action.
    """

    def __init__(self, cli_args, config_dir):

        super().__init__(cli_args, config_dir)

        if self._args.config_action == 'node':
            if self._args.config_node_action == 'add':

                try:
                    with open(self._args.pubkey, 'rb') as key:
                        key_blob = key.read()
                except IOError:
                    print('Failed: the specified public key does not exist', file=sys.stderr)
                    sys.exit(64)

                gpg = GPG(gnupghome=os.path.join(config_dir, 'gpg'))
                result = gpg.import_keys(key_blob)
                try:
                    key_fingerprint = result.fingerprints[0]
                except IndexError:
                    print('Failed: the specified public key was not a valid public key', file=sys.stderr)
                    sys.exit(64)

                try:
                    self._config.add_section(self._args.name)
                    self._config.set(self._args.name, 'addr',   self._args.addr)
                    self._config.set(self._args.name, 'pubkey', key_fingerprint)
                except configparser.DuplicateSectionError:
                    print('Failed: a node with the specified name already exists', file=sys.stderr)
                    sys.exit(64)

            elif self._args.config_node_action == 'rm':
                if not self._config.remove_section(self._args.name):
                    print('Failed: no server exists with the specified name')
                    sys.exit(64)

            with open(os.path.join(self._config_dir, 'servers.ini'), 'w') as config_file:
                self._config.write(config_file)

    def init_subparser(subparser):

        ClientConfigAction._arg_parsers['config'] = subparser
        subparser_factory = subparser.add_subparsers(dest='config_action')
        ClientConfigAction._arg_parsers['config_node'] = subparser_factory.add_parser('node')

        node_subparser_factory = ClientConfigAction._arg_parsers['config_node'].add_subparsers(dest='config_node_action')
        ClientConfigAction._arg_parsers['config_node_add'] = node_subparser_factory.add_parser('add')
        ClientConfigAction._arg_parsers['config_node_rm']  = node_subparser_factory.add_parser('rm')

        ClientConfigAction._arg_parsers['config_node_add'].add_argument('name')
        ClientConfigAction._arg_parsers['config_node_add'].add_argument('addr')
        ClientConfigAction._arg_parsers['config_node_add'].add_argument('pubkey')

        ClientConfigAction._arg_parsers['config_node_rm'].add_argument('name')

        return subparser


class ClientRequestAction(ClientActionBase):
    """
    """


class SimpleClientInterface:
    """
    A simple command line interface for the HyperNova agent.
    """

    actions = {
        'config':  ClientConfigAction,
        'request': ClientRequestAction,
    }

    _arg_parsers = {}

    _config = None

    def __init__(self):
        """
        Perform the action.
        """

        self._init_config()
        self._parse_args()

    def execute(self):
        """
        Run the action.
        """

        self.actions[self.args.action](self.args, self._config_dir)

    def _init_config(self):
        """
        Load the client's configuration.
        """

        self._config_dir  = os.path.join(os.getenv('HOME'), '.hypernova')
        self._config_file = os.path.join(self._config_dir, 'servers.ini')

        try:
            self._config = ConfigurationFactory.get('hypernova',
                                                    root_dir=self._config_file)
        except:
            print('Creating configuration in %s' %(self._config_dir), file=sys.stderr)
            self._init_config_runonce(self._config_dir)

            self._config = ConfigurationFactory.get('hypernova',
                                                    root_dir=self._config_file)

    def _init_config_runonce(self, conf_dir):
        """
        Initialise the configuration directory.

        Calling this on subsequent executions wouldn't be wise, unless, that is,
        you want to implode the user's configuration? ;)
        """

        dirs  = ['gpg']
        files = ['servers.ini']

        os.mkdir(conf_dir, 0o0700)

        for d in dirs:
            os.mkdir(os.path.join(conf_dir, d), 0o0700)

        for f in files:
            path = os.path.join(conf_dir, f)
            with open(path, 'w') as handle:
                handle.write(' ')
            os.chmod(path, 0o0600)

    def _parse_args(self):
        """
        Parse arguments.
        """

        self._arg_parsers['__main__'] = argparse.ArgumentParser(
                description='command line client for the HyperNova agent')
        self.subparser_factory = self._arg_parsers['__main__'].add_subparsers(dest='action')

        for (action, Klass) in self.actions.items():
            self._arg_parsers[action] = self.subparser_factory.add_parser(action)
            Klass.init_subparser(self._arg_parsers[action])

        self.args = self._arg_parsers['__main__'].parse_args()


if __name__ == '__main__':
    SimpleClientInterface().execute()
