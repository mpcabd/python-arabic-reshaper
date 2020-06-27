#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

import os

exec(
    open(os.path.join(
        os.path.dirname(__file__),
        'arabic_reshaper',
        '__version__.py'
    )).read()
)

setup(
    name="arabic_reshaper",
    description=("Reconstruct Arabic sentences to be used in"
                 " applications that don't support Arabic"),
    version=__version__,
    platforms="ALL",
    license="MIT",
    packages=['arabic_reshaper'],
    install_requires=['configparser; python_version <"3"',
                      'future',
                      'setuptools'],
    extras_require={
        'with-fonttools': ['fonttools>=4.0; python_version >="3"',
                           'fonttools>=3.0<4.0; python_version <"3"']
    },
    author="Abdullah Diab",
    author_email="mpcabd@gmail.com",
    maintainer="Abdullah Diab",
    maintainer_email="mpcabd@gmail.com",
    package_dir={'arabic_reshaper': 'arabic_reshaper'},
    package_data={'arabic_reshaper': ['default-config.ini']},
    test_suite='arabic_reshaper.tests',
    include_package_data=True,
    keywords="arabic shaping reshaping reshaper",
    url="https://mpcabd.xyz/python-arabic-text-reshaper/",
    download_url=("https://github.com/mpcabd/"
                  "python-arabic-reshaper/tarball/master"),
    classifiers=[
        "Natural Language :: Arabic",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
