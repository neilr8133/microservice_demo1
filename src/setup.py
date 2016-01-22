#!/bin/env python
#
# @file setup.py
# Setup and configuration required to run the program.

from setuptools import setup, find_packages
setup(
	# Metadata
	author = "Neil Richardson",
	author_email = "neilr@ieee.org",
	description = "Dummy project demonstrating Python use and API construction",
	name = "API_demo",
	version = "0.0.1",
	
	install_requires = [
		'flask',
		'httpie',
		'nose',
		'pylint',
		'requests',
	],
	packages = find_packages(),
	# scripts = [
		# 'main.py',
	# ],
)

# EOF
