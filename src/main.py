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
	httpd_obj = simple_engine.createHttpServer()
	print "Starting single-threaded server..."
	for i in range(2):
		httpd_obj.handle_request()
	print "Reached max number of queries, halting."


if "__main__" == __name__:
	main()

# EOF
