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

from .letters import (UNSHAPED, ISOLATED, LETTERS_ARABIC)
from .ligatures import (SENTENCES_LIGATURES,
                        WORDS_LIGATURES,
                        LETTERS_LIGATURES)

try:
    from fontTools.ttLib import TTFont
    with_font_config = True
except ImportError:
    with_font_config = False

ENABLE_NO_LIGATURES = 0b000
ENABLE_SENTENCES_LIGATURES = 0b001
ENABLE_WORDS_LIGATURES = 0b010
ENABLE_LETTERS_LIGATURES = 0b100
ENABLE_ALL_LIGATURES = 0b111


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


def config_for_true_type_font(font_file_path,
                              ligatures_config=ENABLE_ALL_LIGATURES):
    if not with_font_config:
        raise Exception('fonttools not installed, ' +
                        'install it then rerun this.\n' +
                        '$ pip install arabic-teshaper[with-fonttools]')
    if not font_file_path or not os.path.exists(font_file_path):
        raise Exception('Invalid path to font file')
    ttfont = TTFont(font_file_path)
    has_isolated = True
    for k, v in LETTERS_ARABIC.items():
        for table in ttfont['cmap'].tables:
            if ord(v[ISOLATED]) in table.cmap:
                break
        else:
            has_isolated = False
            break

    configuration = {
        'use_unshaped_instead_of_isolated': not has_isolated,
    }

    def process_ligatures(ligatures):
        for ligature in ligatures:
            forms = list(filter(lambda form: form != '', ligature[1][1]))
            n = len(forms)
            for form in forms:
                for table in ttfont['cmap'].tables:
                    if ord(form) in table.cmap:
                        n -= 1
                        break
            configuration[ligature[0]] = (n == 0)

    if ENABLE_SENTENCES_LIGATURES & ligatures_config:
        process_ligatures(SENTENCES_LIGATURES)

    if ENABLE_WORDS_LIGATURES & ligatures_config:
        process_ligatures(WORDS_LIGATURES)

    if ENABLE_LETTERS_LIGATURES & ligatures_config:
        process_ligatures(LETTERS_LIGATURES)

    return configuration
