#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

import io
import os

with io.open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='arabic_reshaper',
    description=('Reconstruct Arabic sentences to be used in'
                 ' applications that do not support Arabic'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='3.0.0',
    platforms='ALL',
    license='MIT',
    packages=['arabic_reshaper'],
    extras_require={
        'with-fonttools': ['fonttools>=4.0']
    },
    author='Abdullah Diab',
    author_email='mpcabd@gmail.com',
    maintainer='Abdullah Diab',
    maintainer_email='mpcabd@gmail.com',
    package_dir={'arabic_reshaper': 'arabic_reshaper'},
    test_suite='arabic_reshaper.tests',
    include_package_data=True,
    keywords='arabic shaping reshaping reshaper',
    url='https://github.com/mpcabd/python-arabic-reshaper/',
    download_url=('https://github.com/mpcabd/'
                  'python-arabic-reshaper/tarball/master'),
    classifiers=[
        'Natural Language :: Arabic',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
