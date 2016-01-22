#!/bin/env python
#
# Create a simple REST API and attempt to show what you consider ``best practices''.

# Import standard libraries
import BaseHTTPServer

# Import third-party libraries
# (None)

# Import custom libraries
import simple_engine


def main():
	httpd_obj = simple_engine.simpleHttpServer()
	print "Starting single-threaded server..."
	while httpd_obj.get_keep_running():
		httpd_obj.handle_request()
	print "Received request for shutdown; halting."


if "__main__" == __name__:
	main()

# EOF
