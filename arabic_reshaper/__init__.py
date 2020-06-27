import os

from .arabic_reshaper import reshape, default_reshaper, ArabicReshaper
from .reshaper_config import config_for_font


exec(open(os.path.join(os.path.dirname(__file__), '__version__.py')).read())
