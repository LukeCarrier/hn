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
from hypernova.libraries.gnupg import GPG
from hypernova.libraries.client import Client
from hypernova.libraries.configuration import ConfigurationFactory, LoadError
from hypernova import modules
import os
import sys
from  hypernova.libraries.debug import debug_setup

class ClientActionBase:
    """
    Base class for all actions within the client.
    """

    _arg_parsers = {}
    _args        = None

    _config  = None
    _servers = None

    def __init__(self, cli_args, config_dir):
        """
        Run the action.
        """

        self._args = cli_args

        self._config_dir = config_dir
        self._config     = ConfigurationFactory.get('hypernova')
        self._servers    = ConfigurationFactory.get('hypernova.servers')

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
        """
        TODO: break this stupidly huge method down
        """

        super().__init__(cli_args, config_dir)

        if self._args.config_action == 'key':
            try:
                with open(self._args.privkey, 'rb') as key:
                    key_blob = key.read()
            except IOError:
                print('Failed: the specified private key does not exist',
                      file=sys.stderr)
                sys.exit(64)

            gpg = GPG(gnupghome=os.path.join(config_dir, 'gpg'))
            result = gpg.import_keys(key_blob)
            try:
                if not self._config.has_section('client'):
                    self._config.add_section('client')
                self._config['client']['privkey'] = result.fingerprints[0]

            except IndexError:
                print('Failed: the specified private key is invalid')

            with open(os.path.join(config_dir, 'client.ini'), 'w') as c:
                self._config.write(c)

        elif self._args.config_action == 'node':
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
                    gpg.sign_key(result.fingerprints[0])
                    gpg.trust_key(result.fingerprints[0])
                except IndexError:
                    print('Failed: the specified public key is invalid', file=sys.stderr)
                    sys.exit(64)

                try:
                    (addr, port) = self._args.addr.rsplit(':')
                except ValueError:
                    (addr, port) = (self._args.addr, "3030")

                try:
                    self._servers.add_section(self._args.name)
                    self._servers.set(self._args.name, 'addr',   "%s:%s" %(addr, port))
                    self._servers.set(self._args.name, 'pubkey', key_fingerprint)
                except configparser.DuplicateSectionError:
                    print('Failed: a node with the specified name already exists', file=sys.stderr)
                    sys.exit(64)

            elif self._args.config_node_action == 'list':
                for (name, node) in self._servers.items():
                    if name == 'DEFAULT':
                        continue

                    print(name)
                    print('    Address:', node.get('addr'))
                    print('Fingerprint:', node.get('pubkey'))
                    print(' ')

            elif self._args.config_node_action == 'rm':
                if not self._servers.remove_section(self._args.name):
                    print('Failed: no server exists with the specified name')
                    sys.exit(64)

            elif self._args.config_node_action == 'show':
                try:
                    node = self._servers[self._args.name]
                    print(self._args.name)
                    print('    Address:', node['addr'])
                    print('Fingerprint:', node['pubkey'])
                except IndexError:
                    print('Failed: no server exists with the specified name')
                    sys.exit(64)

            with open(os.path.join(self._config_dir, 'servers.ini'), 'w') as f:
                self._servers.write(f)

    def init_subparser(subparser):

        ClientConfigAction._arg_parsers['config'] = subparser
        subparser_factory = subparser.add_subparsers(dest='config_action')

        ClientConfigAction._arg_parsers['config_key'] = subparser_factory.add_parser('key')
        ClientConfigAction._arg_parsers['config_key'].add_argument('privkey')

        ClientConfigAction._arg_parsers['config_node'] = subparser_factory.add_parser('node')
        node_subparser_factory = ClientConfigAction._arg_parsers['config_node'].add_subparsers(dest='config_node_action')

        # Subparsers for actions
        for sp in ['add', 'list', 'rm', 'show']:
            ClientConfigAction._arg_parsers['config_node_' + sp] = \
                    node_subparser_factory.add_parser(sp)

        # Arguments for the above subparsers
        for spa in ['name', 'addr', 'pubkey']:
            ClientConfigAction._arg_parsers['config_node_add'].add_argument(spa)
        ClientConfigAction._arg_parsers['config_node_rm'].add_argument('name')
        ClientConfigAction._arg_parsers['config_node_show'].add_argument('name')

        return subparser


class ClientRequestAction(ClientActionBase):
    """
    Request action handler.
    """

    RESPONSE_FORMATTER_ERROR = "Failed: the response formatter in module '%s'" \
                               " returned an unexpected result"

    def __init__(self, cli_args, config_dir):

        super().__init__(cli_args, config_dir)

        try:
            node = self._servers[cli_args.node]
        except KeyError:
            print('Failed: no server exists with the specified name',
                  file=sys.stderr)
            sys.exit(64)

        (host, sep, port) = node['addr'].partition(':')
        client = Client(host, port, cli_args.gpg_dir)

        module             = getattr(modules, cli_args.request_module)
        RequestBuilder     = getattr(module, 'ClientRequestBuilder')
        request_builder    = getattr(RequestBuilder,
                                     'do_' + cli_args.request_action)
        ResponseFormatter  = getattr(module, 'ClientResponseFormatter')
        response_formatter = getattr(ResponseFormatter,
                                     'do_' + cli_args.request_action)

        request  = request_builder(cli_args, client)
        try:
            keys     = (self._config['client']['privkey'], node['pubkey'])
        except KeyError:
            print("Failed: no private key configured")
            sys.exit(1)
        response = client.query(request, *keys)

        result = response_formatter(cli_args, response)

        # len() raises TypeErrors on NoneType descendants
        try:
            items  = len(result)
        except TypeError:
            print(self.RESPONSE_FORMATTER_ERROR %(cli_args.request_module))
            sys.exit(69)

        if isinstance(result, str) or items == 1:
            print(result)
            sys.exit(0)
        elif items == 2:
            print(result[1])
            sys.exit(result[0])
        else:
            print(self.RESPONSE_FORMATTER_ERROR %(cli_args.request_module))
            sys.exit(69)


    def init_subparser(subparser):

        gpg_dir = os.path.join(os.getenv('HOME'), '.hypernova', 'gpg')
        subparser.add_argument('--gpg-dir', dest='gpg_dir', default=gpg_dir)

        subparser.add_argument('node')

        subparser_factory = subparser.add_subparsers(dest='request_module')

        for module in modules.__all__:
            pymodule = getattr(modules, module)

            try:
                Klass = getattr(pymodule, 'ClientRequestBuilder')
                ClientRequestAction._arg_parsers['request_' + module] = \
                    module_subparser = subparser_factory.add_parser(module)
                module_subparser_factory = \
                        module_subparser.add_subparsers(dest='request_action')
                Klass.init_subparser(module_subparser, module_subparser_factory)

            except AttributeError:
                print('Error: module %s contains no interface definition'
                      %(module), file=sys.stderr)

        return subparser


class SimpleClientInterface:
    """
    A simple command line interface for the HyperNova agent.
    """

    actions = {
        'config':  ClientConfigAction,
        'request': ClientRequestAction,
    }

    _arg_parsers = {}

    _config  = None
    _servers = None

    _config_file  = ''
    _servers_file = ''

    def __init__(self, config_dir=None):
        """
        Perform the action.
        """

        if config_dir:
            self._config_dir = os.path.abspath(config_dir)
        else:
            self._config_dir = os.path.join(os.getenv('HOME'), '.hypernova')

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

        self._config_file  = os.path.join(self._config_dir, 'client.ini')
        self._servers_file = os.path.join(self._config_dir, 'servers.ini')

        try:
            os.listdir(self._config_dir)
        except (LoadError, OSError):
            print('Creating configuration in %s' %(self._config_dir), file=sys.stderr)
            self._init_config_runonce(self._config_dir)
        finally:
            self._config = ConfigurationFactory.get('hypernova',
                                                    root_dir=self._config_file)
            self._servers = ConfigurationFactory.get('hypernova.servers',
                                                     root_dir=self._servers_file)

    def _init_config_runonce(self, conf_dir):
        """
        Initialise the configuration directory.

        Calling this on subsequent executions wouldn't be wise, unless, that is,
        you want to implode the user's configuration? ;)
        """

        dirs  = ['gpg']
        files = ['client.ini', 'servers.ini']

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
    try:
        debug_setup()
        config_dir = os.getenv('CONFDIR')
    except KeyError:
        config_dir = None

    SimpleClientInterface(config_dir).execute()
