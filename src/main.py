#!/bin/env python
#
# Create a simple REST API and attempt to show what you consider ``best practices''.

# Import standard libraries
import ConfigParser

# Import third-party libraries
# (None)

# Import custom libraries
#import frameworks.simple_engine as engine
import frameworks.flask_engine as engine


def yes():
	return 'Yes'

def no():
	return 'No'

def parse_options():
	master_config = 'config.ini'
	config = {}
	parser = ConfigParser.SafeConfigParser()
	parser.read(master_config)
	config['bind_address'] = parser.get('master', 'bind_address')
	config['listen_port'] = parser.getint('master', 'listen_port')
	return config
# End of parse_options() -----------------------------------------------------


def main():
	config = parse_options()
	httpd_obj = engine.simpleHttpServer(
			config['bind_address'],
			config['listen_port']
	)
	httpd_obj.register_endpoint('/yes', yes)
	httpd_obj.register_endpoint('/no', no)
	print "Starting single-threaded server on {0}:{1}".format(
			config['bind_address'],
			config['listen_port']
	)
	while httpd_obj.get_keep_running():
		httpd_obj.handle_request()
	print "Received request for shutdown; halting."
# End of main() --------------------------------------------------------------


if "__main__" == __name__:
	main()

# EOF
