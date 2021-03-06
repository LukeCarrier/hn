#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# WordPress site management
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import re
from hypernova.libraries.siteconfig import SiteConfigBase, SiteProvisionerBase
from os.path import join

class SiteConfig(SiteConfigBase):
    """
    WordPress site configuration.

    This object represents a standard wp-config.php file. Its __str__() method
    converts into such.

    When making changes to this file, be sure to carefully examine the
    appropriate documentation before hand to ensure you fully understand the
    effects of your changes! This is usually a good place to start research:

        http://codex.wordpress.org/Editing_wp-config.php
    """

    # Support DB character sets; UTF-8 only for now
    DB_CHARSETS = [
        'utf8'
    ]

    # Database credentials
    db_host        = ''
    db_username    = ''
    db_password    = ''
    db_name        = ''
    db_prefix      = ''
    db_charset     = ''
    db_auto_repair = None

    # Hash key/salt values
    #
    # I doubt anybody fully understands what all of these control, but they
    # should all be random for security reasons.
    key_auth         = ''
    key_secure_auth  = ''
    key_logged_in    = ''
    key_nonce        = ''
    salt_auth        = ''
    salt_secure_auth = ''
    salt_logged_in   = ''
    salt_nonce       = ''

    # Site location details
    site_url      = ''
    site_home     = ''

    # Authentication/session options
    cookie_domain       = ''
    cookie_path         = ''
    site_cookie_path    = ''
    admin_cookie_path   = ''
    plugin_cookie_path  = ''

    # Content directory location
    content_dir = ''
    content_url = ''

    # Content (stylesheets, JavaScript, etc) editing
    content_enable_modifications = None

    # Explosive options that should never, ever, ever (in your wildest dreams)
    # be changed
    template_path   = ''
    stylesheet_path = ''

    # Plugin directory location
    #
    # The plugin_url value has to be set in two places for some older plugins.
    # We set PLUGINDIR *and* WP_PLUGIN_DIR to ensure no ill effects.
    plugin_dir = ''
    plugin_url = ''

    # Post/page revision control
    #
    # To limit the number of revisions that can be stored, you can change the
    # value of revisions_max_stored to any integer value above zero. Setting it
    # to true implies infinity. A value of false completely disables revisions.
    # To disable compacting ("trash emptying"), set
    # revisions_compact to zero.
    revisions_autosave_interval = None
    revisions_max_stored        = None
    revisions_compact           = None

    # Multi-site installation?
    #
    # This is best left false (the default) for most installations.
    is_multisite = None

    # Debugging configuration
    #
    # The server option, when true, displays error messages and warnings
    # generated by WordPress and its plugins. The client option does the same,
    # but for the client side code (JavaScript).
    debug_server         = None
    debug_server_display = None
    debug_server_log     = None
    debug_db             = None
    debug_client         = None

    # Optimisations
    concatenate_admin_js = None
    cache                = None
    cron_enable          = None
    cron_alternate       = None

    # Integration options
    #
    # Setting these values to None will cause them to be omitted, forcing the
    # defaults.
    integration_user_table     = None
    integration_usermeta_table = None

    # Internationalisation/localisation
    lang     = ''
    lang_dir = ''

    # Filesystem permission options
    chmod_dir  = None
    chmod_file = None

    # Upgrade configuration
    #
    # We should research effectively disabling this for specified sites, so as
    # to prevent upgrades breaking things before plugins have been updated. For
    # now, these options are best left set to false.
    #
    # When working with larger sites, the upgrade_global_db_tables functionality
    # should *definitely* be disabled to prevent breaking production sites. A
    # better approach than applying these major, potentially slow, upgrades via
    # PHP would be to perform the upgrade manually through MySQL's batch
    # processing, then redeploy the site's files and upgraded database when
    # complete.
    upgrade_method           = ''
    upgrade_global_db_tables = None
    ftp_host                 = ''
    ftp_ssl                  = None
    ftp_base                 = ''
    ftp_content_dir          = ''
    ftp_plugin_dir           = ''
    ftp_key_pub              = ''
    ftp_key_priv             = ''
    ftp_username             = ''
    ftp_password             = ''

    __templ_option = "define('%s', %s);"
    __file_pre = """<?php
/*
 * Generated by HyperNova (hypernova.libraries.siteconfig.wordpress)
 *
 * This file was automatically generated and any modifications made to it will
 * likely be overwritten by automated maintenance. For assistance, contact our
 * support department.
 */
"""
    __file_post = """
$table_prefix = defined('TABLE_PREFIX') ? TABLE_PREFIX : '';

if (!defined('ABSPATH'))
    define('ABSPATH', (dirname(__FILE__) . DIRECTORY_SEPARATOR));

require_once(ABSPATH . 'wp-settings.php');
"""

    __mapping = {
        'db_host':        'DB_HOST',
        'db_username':    'DB_USER',
        'db_password':    'DB_PASSWORD',
        'db_name':        'DB_NAME',
        'db_prefix':      'DB_PREFIX',
        'db_charset':     'DB_CHARSET',
        'db_auto_repair': 'WP_ALLOW_REPAIR',

        'key_auth':         'AUTH_KEY',
        'key_secure_auth':  'SECURE_AUTH_KEY',
        'key_logged_in':    'LOGGED_IN_KEY',
        'key_nonce':        'NONCE_KEY',
        'salt_auth':        'AUTH_SALT',
        'salt_secure_auth': 'SECURE_AUTH_SALT',
        'salt_logged_in':   'LOGGED_IN_SALT',
        'salt_nonce':       'NONCE_SALT',

        'site_url':  'WP_SITEURL',
        'site_home': 'WP_HOME',

        'cookie_domain':      'COOKIE_DOMAIN',
        'cookie_path':        'COOKIEPATH',
        'site_cookie_path':   'SITECOOKIEPATH',
        'admin_cookie_path':  'ADMIN_COOKIE_PATH',
        'plugin_cookie_path': 'PLUGINS_COOKIE_PATH',

        'content_dir': 'WP_CONTENT_DIR',
        'content_url': 'WP_CONTENT_URL',

        'content_enable_modifications': 'DISALLOW_FILE_MODS',

        'template_path':   'TEMPLATEPATH',
        'stylesheet_path': 'STYLESHEETPATH',

        'plugin_dir': 'WP_PLUGIN_DIR',
        'plugin_url': 'WP_PLUGIN_URL',

        'revisions_autosave_interval': 'AUTOSAVE_INTERVAL',
        'revisions_max_stored':        'WP_POST_REVISIONS',
        'revisions_compact':           'EMPTY_TRASH_DAYS',

        'debug_server':         'WP_DEBUG',
        'debug_server_display': 'WP_DEBUG_DISPLAY',
        'debug_server_log':     'WP_DEBUG_LOG',
        'debug_db':             'SAVEQUERIES',
        'debug_client':         'SCRIPT_DEBUG',

        'concatenate_admin_js': 'CONCATENATE_SCRIPTS',
        'cache':                'WP_CACHE',
        'cron_enable':          'DISABLE_WP_CRON',
        'cron_alternate':       'ALTERNATE_WP_CRON',

        'integration_user_table':     'CUSTOM_USER_TABLE',
        'integration_usermeta_table': 'CUSTOM_USER_META_TABLE',

        'lang':     'WP_LANG',
        'lang_dir': 'WP_LANG_DIR',

        'chmod_dir':  'FS_CHMOD_DIR',
        'chmod_file': 'FS_CHMOD_FILE',

        'upgrade_method':           'FS_METHOD',
        'upgrade_global_db_tables': 'DO_NOT_UPGRADE_GLOBAL_TABLES',
        'ftp_host':                 'FTP_HOST',
        'ftp_ssl':                  'FTP_SSL',
        'ftp_base':                 'FTP_BASE',
        'ftp_content_dir':          'FTP_CONTENT_DIR',
        'ftp_plugin_dir':           'FTP_PLUGIN_DIR',
        'ftp_key_pub':              'FTP_PUBKEY',
        'ftp_key_priv':             'FTP_PRIVKEY',
        'ftp_username':             'FTP_USER',
        'ftp_password':             'FTP_PASS',
    }

    # Booleans that actually make sense
    __bools = [
        'db_auto_repair',
        'debug_server',
        'debug_server_display',
        'debug_server_log',
        'debug_db',
        'debug_client',
        'concatenate_admin_js',
        'cache',
        'cron_alternative',
    ]

    # Booleans that start with disable/don't
    __reverse_bools = [
        'content_enable_modifications',
        'cron_enable',
        'upgrade_global_db_tables',
    ]

    __ints = [
        'revisions_autosave_interval',
        'revisions_compact',
        'chmod_dir',
    ]

    def __php_boolean(self, value):
        """
        Format a Python boolean into a PHP one.
        """

        if value:
            return 'true'

        return 'false'

    def __php_str(self, value):
        """
        Format a Python string as a PHP one.
        """

        return '\'' + re.sub(r'[\\\']', r'\\\\\'', value) + '\''

    def __init__(self):
        """
        Initialise defaults.
        """

    def __str__(self):
        options = []
        for abstract, actual in self.__mapping.items():
            value = getattr(self, abstract)

            if not value:
                continue
            elif abstract in self.__bools:
                value = self.__php_boolean(value)
            elif abstract in self.__reverse_bools:
                value = self.__php_boolean(not value)
            elif not value:
                continue
            else:
                value = self.__php_str(str(value))

            options.append(self.__templ_option %(actual, value))

        return "\n".join([
            self.__file_pre,
            "\n".join(options),
            self.__file_post,
        ])

class SiteProvisioner(SiteProvisionerBase):
    """
    WordPress provisioner.
    """

    module_name = 'wordpress'

    __source_url        = 'http://wordpress.org/wordpress-%s.tar.gz'
    __latest_source_url = 'http://wordpress.org/latest.tar.gz'

    source_url = None

    def __init__(self, *args):
        super().__init__(*args)

        self.domain_name = self.parameters[0]

        try:
            self.source_url = self.__source_url %(self.parameters[1])
        except IndexError:
            self.source_url = self.__latest_source_url

    def _provision(self):

        print('downloading source...')
        tarball = self.download_url(self.source_url, provider='HTTP',
                                    suffix='.tar.gz')
        print(' =>', tarball)

        print('extracting source...')
        source = self.extract_gzipped_tarball(tarball)
        print(' =>', source)

        print('creating system user account...')
        user = self.create_system_user()
        print(' => username:', user.account)
        print(' => password:', user.password)

        # We now have all the data we need to know the substitutions we can
        # apply to formatting strings
        substitutions = {
            "domainname": self.domain_name,
            "homedir":    user.directory,
            "username":   user.account,
        }

        print('creating database...')
        db = self.create_mysql_database()
        print(' => username:', db['user'].username)
        print(' => password:', db['user'].password)
        print(' => database:', db['database'].name)

        # Use Python-native interpolation instead of the functionality
        # implemented in configparser to avoid accidentally substituting values
        # from the user's config; they *must* come from the user object
        print('installing source...')
        target = self.config.get('web', 'base_dir', raw=True)
        print(' => skeleton:', target)
        target = target.format(**substitutions)
        print(' => resulting path:', target)
        self.move_tree(join(source, 'wordpress'), target)

        print('configuring web server...')
        vhost = self.add_vhost()
        vhost.document_root = target
        vhost.listen = 80
        vhost.server_names = [self.domain_name]
        vhost.indexes = ['index.php', 'index.html', 'index.htm']
        vhost.includes.append('enable_php')
        self.create_vhost(vhost, file_substitutions=substitutions)

        print('configuring application...')
        config = SiteConfig()

        config.db_host     = db['user'].host
        config.db_username = db['user'].username
        config.db_password = db['user'].password
        config.db_name     = db['database'].name
        config.db_prefix   = 'wp_'
        config.db_charset  = SiteConfig.DB_CHARSETS[0]
        config.db_collate  = ''

        for k in ['auth', 'secure_auth', 'nonce', 'logged_in']:
            for t in ['key', 'salt']:
                setattr(config, '%s_%s' %(t, k), self._random_string(64))

        with open(join(target, 'wp-config.php'), 'w') as f:
            f.write(str(config))

        # Set file permissions
        print('securing file permissions...')
        self.set_document_root_permissions(
            user, self.get_web_group(), vhost,
            self.config.getboolean("web", "acl_group"))
