#!/bin/env python
#
# Create a simple REST API and attempt to show what you consider ``best practices''.

# Import standard libraries
# (None)

# Import third-party libraries
# (None)

# Import custom libraries
import frameworks.simple_engine as simple_engine


def yes():
	return 'Yes'

def no():
	return 'No'

def main():
	httpd_obj = simple_engine.simpleHttpServer()
	httpd_obj.register_endpoint('/yes', yes)
	httpd_obj.register_endpoint('/no', no)
	print "Starting single-threaded server..."
	while httpd_obj.get_keep_running():
		httpd_obj.handle_request()
	print "Received request for shutdown; halting."


if "__main__" == __name__:
	main()

# EOF
