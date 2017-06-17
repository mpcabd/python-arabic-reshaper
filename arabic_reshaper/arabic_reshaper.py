# -*- coding: utf-8 -*-

# This work is licensed under the GNU Public License (GPL).
# To view a copy of this license, visit http://www.gnu.org/copyleft/gpl.html

# Written by Abdullah Diab (mpcabd)
# Email: mpcabd@gmail.com
# Website: http://mpcabd.xyz

# Ported and tweaked from Java to Python, from Better Arabic Reshaper
# [https://github.com/agawish/Better-Arabic-Reshaper/]

# Usage:
# Install python-bidi [https://github.com/MeirKriheli/python-bidi], can be
# installed from pip `pip install python-bidi`.

# import arabic_reshaper
# from bidi.algorithm import get_display
# reshaped_text = arabic_reshaper.reshape('اللغة العربية رائعة')
# bidi_text = get_display(reshaped_text)
# Now you can pass `bidi_text` to any function that handles
# displaying/printing of the text, like writing it to PIL Image or passing it
# to a PDF generating method.

from __future__ import unicode_literals
from builtins import range

import re
import os

from configparser import ConfigParser
from itertools import repeat
from pkg_resources import resource_filename

from .ligatures import *
from .letters import *

HARAKAT_RE = re.compile(
    '['
    '\u0610-\u061a'
    '\u064b-\u065f'
    '\u0670'
    '\u06d6-\u06dc'
    '\u06df-\u06e8'
    '\u06ea-\u06ed'
    '\u08d4-\u08e1'
    '\u08d4-\u08ed'
    '\u08e3-\u08ff'
    ']',

    re.UNICODE | re.X
)


class ArabicReshaper(object):
    """
    A class for Arabic reshaper, it allows for fine-tune configuration over the
    API.

    If no configuration is passed to the constructor, the class will check for
    an environment variable :envvar:`PYTHON_ARABIC_RESHAPER_CONFIGURATION_FILE`
    , if the variable is available, the class will load the file pointed to by
    the variable, and will read it as an ini file.
    If the variable doesn't exist, the class will load with the default
    configuration file :file:`default-config.ini`

    Check these links for information on the configuration files format:

    * Python 3: https://docs.python.org/3/library/configparser.html
    * Python 2: https://docs.python.org/2/library/configparser.html

    See the default configuration file :file:`default-config.ini` for details
    on how to configure your reshaper.
    """
    def __init__(self, configuration=None, configuration_file=None):
        super(ArabicReshaper, self).__init__()

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
        configuration_from_files = configuration_parser.read(
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

        configuration = configuration_parser['ArabicReshaper']
        self.configuration = configuration

    @property
    def _ligatures_re(self):
        if not hasattr(self, '__ligatures_re'):
            patterns = []
            re_group_index_to_ligature_forms = {}
            index = 0
            FORMS = 1
            MATCH = 0
            for ligature_record in LIGATURES:
                ligature, replacement = ligature_record
                if not self.configuration.getboolean(ligature):
                    continue
                re_group_index_to_ligature_forms[index] = replacement[FORMS]
                patterns.append('({})'.format(replacement[MATCH]))
                index += 1
            self._re_group_index_to_ligature_forms = (
                re_group_index_to_ligature_forms
            )
            self.__ligatures_re = re.compile('|'.join(patterns), re.UNICODE)
        return self.__ligatures_re

    def _get_ligature_forms_from_re_group_index(self, group_index):
        if not hasattr(self, '_re_group_index_to_ligature_forms'):
            self._ligatures_re
        return self._re_group_index_to_ligature_forms[group_index]

    def reshape(self, text):
        if not text:
            return ''

        output = []

        LETTER = 0
        FORM = 1
        NOT_SUPPORTED = -1

        delete_harakat = self.configuration.getboolean('delete_harakat')
        delete_tatweel = self.configuration.getboolean('delete_tatweel')
        positions_harakat = {}

        for letter in text:
            if HARAKAT_RE.match(letter):
                if not delete_harakat:
                    position = len(output) - 1
                    if position not in positions_harakat:
                        positions_harakat[position] = []
                    positions_harakat[position].append(letter)
            elif letter == TATWEEL and delete_tatweel:
                pass
            elif letter not in LETTERS:
                output.append((letter, NOT_SUPPORTED))
            elif not output:
                output.append((letter, ISOLATED))
            else:
                previous_letter = output[-1]
                if previous_letter[FORM] == NOT_SUPPORTED:
                    output.append((letter, ISOLATED))
                elif not connects_with_letter_before(letter):
                    output.append((letter, ISOLATED))
                elif not connects_with_letter_after(
                    previous_letter[LETTER]
                ):
                    output.append((letter, ISOLATED))
                elif (previous_letter[FORM] == FINAL and not
                      connects_with_letters_before_and_after(
                          previous_letter[LETTER]
                      )):
                    output.append((letter, ISOLATED))
                elif previous_letter[FORM] == ISOLATED:
                    output[-1] = (
                        previous_letter[LETTER],
                        INITIAL
                    )
                    output.append((letter, FINAL))
                # Otherwise, we will change the previous letter to connect
                # to the current letter
                else:
                    output[-1] = (
                        previous_letter[LETTER],
                        MEDIAL
                    )
                    output.append((letter, FINAL))

        if self.configuration.getboolean('support_ligatures'):
            # Clean text from Harakat to be able to find ligatures
            text = HARAKAT_RE.sub('', text)

            # Clean text from Tatweel to find ligatures if delete_tatweel
            if delete_tatweel:
                text = text.replace(TATWEEL, '')

            for match in re.finditer(self._ligatures_re, text):
                group_index = next((
                    i for i, group in enumerate(match.groups()) if group
                ), -1)
                forms = self._get_ligature_forms_from_re_group_index(
                    group_index
                )
                a, b = match.span()
                a_form = output[a][FORM]
                b_form = output[b - 1][FORM]
                ligature_form = None

                # +-----------+----------+---------+---------+----------+
                # | a   \   b | ISOLATED | INITIAL | MEDIAL  | FINAL    |
                # +-----------+----------+---------+---------+----------+
                # | ISOLATED  | ISOLATED | INITIAL | INITIAL | ISOLATED |
                # | INITIAL   | ISOLATED | INITIAL | INITIAL | ISOLATED |
                # | MEDIAL    | FINAL    | MEDIAL  | MEDIAL  | FINAL    |
                # | FINAL     | FINAL    | MEDIAL  | MEDIAL  | FINAL    |
                # +-----------+----------+---------+---------+----------+

                if a_form in (ISOLATED, INITIAL):
                    if b_form in (ISOLATED, FINAL):
                        ligature_form = ISOLATED
                    else:
                        ligature_form = INITIAL
                else:
                    if b_form in (ISOLATED, FINAL):
                        ligature_form = FINAL
                    else:
                        ligature_form = MEDIAL
                if not forms[ligature_form]:
                    continue
                output[a] = (forms[ligature_form], NOT_SUPPORTED)
                output[a+1:b] = repeat(('', NOT_SUPPORTED), b - 1 - a)

        result = []
        if not delete_harakat and -1 in positions_harakat:
            result.extend(positions_harakat[-1])
        for i, o in enumerate(output):
            if o[LETTER]:
                if o[FORM] == NOT_SUPPORTED:
                    result.append(o[LETTER])
                else:
                    result.append(LETTERS[o[LETTER]][o[FORM]])

            if not delete_harakat:
                if i in positions_harakat:
                    result.extend(positions_harakat[i])

        return ''.join(result)


default_reshaper = ArabicReshaper()
reshape = default_reshaper.reshape
