#!/usr/bin/env python2
# coding = utf-8


from setuptools import setup

setup( 
	name = "arabic_reshaper",
	description = "Reconstruct Arabic sentences to be used in applications that don't support Arabic",
	version = 1.0,
	platforms = "ALL",
	license = "AGPL",
	packages = ['arabic_reshaper'],
	install_requires = [],

	author = "Abd Allah Diab",
	author_email = "mpcabd ^at^ gmail ^dot^ com",
	maintainer = "Abd Allah Diab",
	maintainer_email = "mpcabd ^at^ gmail ^dot^ com",

	package_dir = {'arabic_reshaper':'.'},
	keywords = "arabic shaping",
url = "http://mpcabd.xyz/python-arabic-text-reshaper/",
download_url = "https://github.com/mpcabd/python-arabic-reshaper/tarball/master",

	classifiers = [
	"Natural Language :: Arabic",
	"Operating System :: OS Independent",
	"Programming Language :: Python :: 2.7",
	"Topic :: Software Development :: Libraries :: Python Modules",
	],
 )
