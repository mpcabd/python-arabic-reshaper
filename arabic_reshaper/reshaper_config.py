# -*- coding: utf-8 -*-

# This work is licensed under the MIT License.
# To view a copy of this license, visit https://opensource.org/licenses/MIT

# Written by Abdullah Diab (mpcabd)
# Email: mpcabd@gmail.com
# Website: http://mpcabd.xyz

from __future__ import unicode_literals

import os

from configparser import ConfigParser
from pkg_resources import resource_filename

def auto_config(configuration=None, configuration_file=None):
    configuration_files = [
        resource_filename(__name__, 'default-config.ini')
    ]

    if not os.path.exists(configuration_files[0]):
        raise Exception(
            ('Default configuration file {} not found,' +
             ' check the module installation.').format(
                 configuration_files[0],
             )
        )

    loaded_from_envvar = False

    if not configuration_file:
        configuration_file = os.getenv(
            'PYTHON_ARABIC_RESHAPER_CONFIGURATION_FILE'
        )
        if configuration_file:
            loaded_from_envvar = True

    if configuration_file:
        if not os.path.exists(configuration_file):
            raise Exception(
                'Configuration file {} not found{}.'.format(
                    configuration_file,
                    loaded_from_envvar and (
                        ' it is set in your environment variable ' +
                        'PYTHON_ARABIC_RESHAPER_CONFIGURATION_FILE'
                    ) or ''
                )
            )
        configuration_files.append(configuration_file)

    configuration_parser = ConfigParser()
    configuration_parser.read(
        configuration_files
    )

    if configuration:
        configuration_parser.read_dict({
            'ArabicReshaper': configuration
        })

    if 'ArabicReshaper' not in configuration_parser:
        raise ValueError(
            'Invalid configuration: '
            'A section with the name ArabicReshaper was not found'
        )

    return configuration_parser['ArabicReshaper']


def config_for_font():
    pass

