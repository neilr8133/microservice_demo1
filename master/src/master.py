from __future__ import absolute_import
#
# @file main.py
#
#
# Create a simple REST API and attempt to show what you consider ``best practices''.
#
# This file launches the 'master' of a master/minion pair.

# Import standard libraries
import ConfigParser

# Import third-party libraries
# (None)

# Import custom libraries
import api
import config
import global_vars
import storage


def main():
	config.parse_options()
	#global_vars.storage_handle = storage.connect(global_vars.db_filename)
	global_vars.app_handle.run(
		host=global_vars.bind_address,
		port=global_vars.listen_port,
		debug=True,
		use_debugger=True,
	)
	#storage.close(global_vars.storage_handle)
	print "Received request for shutdown; halting."
# End of main() --------------------------------------------------------------


if "__main__" == __name__:
	main()

# EOF
