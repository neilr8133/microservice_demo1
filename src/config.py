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
	globals.app_name = parser.get('master', 'app_name')
	globals.db_filename = parser.get('master', 'db_filename')
	globals.bind_address = parser.get('master', 'bind_address')
	globals.listen_port = parser.getint('master', 'listen_port')
	globals.minion_adddress = parser.get('master', 'minion_address')
	globals.minion_port = parser.getint('master', 'minion_port')
# End of parse_options() -----------------------------------------------------

# EOF
