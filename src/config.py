from __future__ import absolute_import
#
# @file config.py
#
# Parse the runtime configuration options.

# Import standard libraries
import ConfigParser

# Import third-party libraries
# (None)

# Import custom libraries
import globals


def parse_options():
	master_config_filename = 'config.ini'
	config = {}
	parser = ConfigParser.SafeConfigParser()
	parser.read(master_config_filename)
	globals.bind_address = parser.get('master', 'bind_address')
	globals.listen_port = parser.getint('master', 'listen_port')
# End of parse_options() -----------------------------------------------------

# EOF
