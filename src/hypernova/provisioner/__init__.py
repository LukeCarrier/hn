#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Provisioner tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.configuration import ConfigurationFactory
import json
import logging
import sys

APPCONFIG_PACKAGE = 'hypernova.libraries.appconfig'
APPCONFIG_CLASS   = 'AppProvisioner'

class Provisioner:
    """
    Provisions service units via the appconfig library.

    Provisioning prevents a challenge, since the intent with the agent was to
    allow it to perform actions that require root privileges _without_ running
    as root itself. In order to enable this separation, the agent calls out to
    the provisioning tool using elevator as a stopgap, which, via the setuid
    filesystem bit, is able to run with the effective privileges of root.

    TODO: lots:
    * isolate the libraries available to provisioning services.
    * provide security token authentication - maybe OTP?
    """

    _config = None

    _module_name = None
    _parameters  = {}

    _main_log           = None
    _main_log_formatter = None
    _main_log_handler   = None

    def __init__(self, config_root_dir, module_name, *params):
        """
        Initialise the configuration parameters.
        """

        self._module_name = module_name
        self._parameters  = params

        self._init_logging();
        self._init_config(config_root_dir)

    def _init_config(self, config_root_dir):
        """
        Initialise configuration values.

        See __init__() for more information.
        """

        self._main_log.info('loading configuration from directory %s'
                            %(config_root_dir))
        self._config = ConfigurationFactory.get('hypernova', config_root_dir,
                                                self._main_log)

        if not self._config:
            self._main_log.critical('loading configuration failed')
            sys.exit(78)

    def _init_logging(self):
        """
        Initialise the logger instances.
        """

        self._main_log_formatter = logging.Formatter(
            fmt = '[%(asctime)s] [%(levelname)-1s] %(message)s',
            datefmt = '%d/%m/%Y %I:%M:%S')

        self._main_log = logging.getLogger('hn-main')
        self._main_log.setLevel(logging.DEBUG)

    def execute(self):
        """
        Perform the provisioning operation.
        """

        global_vars = globals()
        appconfig_pkg = global_vars['APPCONFIG_PACKAGE']
        appconfig_cls = global_vars['APPCONFIG_CLASS']

        module_name = '%s.%s' %(appconfig_pkg, self._module_name)

        app_module = __import__(module_name, fromlist=[appconfig_cls])
        app_provisioner = app_module.AppProvisioner()
        app_provisioner.do_provision(*self._parameters)


if __name__ == '__main__':
    Provisioner(*sys.argv[1:]).execute()
