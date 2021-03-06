#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Package (egg) definition
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from setuptools import setup

import hypernova as hn

setup(
    name             = hn.__friendly_name__,
    version          = hn.__version__,
    description      = hn.__description__,
    author           = hn.__author__,
    author_email     = hn.__author_email__,
    url              = hn.__url__,
    packages         = [
        'hypernova',
        'hypernova.libraries',
        'hypernova.libraries.appconfig',
        'hypernova.libraries.appconfig.authserver',
        'hypernova.libraries.appconfig.dbserver',
        'hypernova.libraries.appconfig.dnsserver',
        'hypernova.libraries.appconfig.httpserver',
        'hypernova.libraries.siteconfig',
        'hypernova.libraries.packagemanagement',
        'hypernova.modules',
    ],
    install_requires = ['python-gnupg'],
    classifiers      = [
        'Programming Language :: Python',
        'Topic :: Internet',
    ],
    keywords         = ['cloud', 'linux', 'management', 'networking',
                        'orchestration', 'system'],
    license          = 'GPL'
)
