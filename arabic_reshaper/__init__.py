import os

from .arabic_reshaper import reshape, default_reshaper, ArabicReshaper
from .reshaper_config import (config_for_true_type_font,
                              ENABLE_NO_LIGATURES,
                              ENABLE_SENTENCES_LIGATURES,
                              ENABLE_WORDS_LIGATURES,
                              ENABLE_LETTERS_LIGATURES,
                              ENABLE_ALL_LIGATURES)


with open(os.path.join(os.path.dirname(__file__), '__version__.py')) as fh:
    exec(fh.read())
