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
	version = "0.3.0",
	
	install_requires = [
		# Only used for development or demo--not required for 'production'
		# (and would probably be removed from a release candidate, although
		# their presence should cause no harm).
		'bumpversion',
		'httpie',
		'nose',
		'pylint',
		
		# Used for 'production'
		'flask',
		'requests',
	],
	packages = find_packages(),
)

# EOF
