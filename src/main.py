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
import globals


def main():
	config.parse_options()
	globals.app.run(
		host=globals.bind_address,
		port=globals.listen_port
	)
	print "Received request for shutdown; halting."
# End of main() --------------------------------------------------------------


if "__main__" == __name__:
	main()

# EOF
