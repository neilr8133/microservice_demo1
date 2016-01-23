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
import globals


def parse_options():
	master_config_filename = 'config.ini'
	config = {}
	parser = ConfigParser.SafeConfigParser()
	parser.read(master_config_filename)
	# config['bind_address'] = parser.get('master', 'bind_address')
	# config['listen_port'] = parser.getint('master', 'listen_port')
	return config
# End of parse_options() -----------------------------------------------------


def main():
	config = parse_options()
	# httpd_obj = engine.simpleHttpServer(
			# config['bind_address'],
			# config['listen_port']
	# )
	# print "Starting single-threaded server on {0}:{1}".format(
			# config['bind_address'],
			# config['listen_port']
	# )
	# while httpd_obj.get_keep_running():
		# httpd_obj.handle_request()
	#app.run()
	globals.app.run()
	print "Received request for shutdown; halting."
# End of main() --------------------------------------------------------------


if "__main__" == __name__:
	main()

# EOF
