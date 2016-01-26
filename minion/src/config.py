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
import global_vars


def parse_options():
	master_config_filename = 'config.ini'
	config = {}
	parser = ConfigParser.SafeConfigParser()
	parser.read(master_config_filename)
	global_vars.app_name = parser.get('master', 'app_name')
	global_vars.db_filename = parser.get('master', 'db_filename')
	global_vars.bind_address = parser.get('master', 'bind_address')
	global_vars.listen_port = parser.getint('master', 'listen_port')
# End of parse_options() -----------------------------------------------------

# EOF
