#!/bin/env python
#
# Create a simple REST API and attempt to show what you consider ``best practices''.

# Import standard libraries
import BaseHTTPServer


class customRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	# Do not override or extend the __init__() method.
	def do_GET(self):
		print "GET request received:"
		print "\tRequest path: {0}".format(self.path)
		print "Sending headers..."
		self.send_response(200)
		self.send_header('queries_answered', 'infinite')
		self.end_headers()
		self.wfile.write("""<HTML><BODY><P>Success!</p></body></html>""")
# End of class customRequestHandler ==========================================



def createHttpServer(server_class=BaseHTTPServer.HTTPServer,
                     handler_class=customRequestHandler):
	"""Creates a simple HTTP server that responds to custom API endpoints.
	
	Based on the documentation sample at
	https://docs.python.org/2.7/library/basehttpserver.html
	
	@return An HTTPD server object (not yet running)
	"""
	server_listen_address = ('127.0.0.1', 8000)  # Only listen to localhost.
	httpd = server_class(server_listen_address, handler_class)
	return httpd
# End of createHttpServer() --------------------------------------------------


def main():
	httpd_obj = createHttpServer()
	print "Starting single-threaded server..."
	for i in range(2):
		httpd_obj.handle_request()


if "__main__" == __name__:
	main()

# EOF
