import os

from .arabic_reshaper import reshape, default_reshaper, ArabicReshaper


exec(open(os.path.join(os.path.dirname(__file__), '__version__.py')).read())
