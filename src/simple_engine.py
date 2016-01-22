#!/bin/env python
#
# Abstract the engine so it can be replaced with a more robust framework

# Import standard libraries
import BaseHTTPServer

# Import third-party libraries
# (None)

# Import custom libraries
# (None)


class customRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	
	# Declare some class-level variables
	_num_queries_received = 0
	_keep_serving_queries = True
	
	# Do not override or extend the __init__() method.
	
	def emit_html_header(self):
		return """
<HTML>
	<HEAD>
		<TITLE>Page demo from builtin engine</TITLE>
	</HEAD>
	<BODY>"""
	
	def emit_html_footer(self):
		return """
	</BODY>
</HTML>"""
	
	
	def do_GET(self):
		print "GET request received:"
		print "\tRequest path: {0}".format(self.path)
		print "Sending headers..."
		customRequestHandler._num_queries_received += 1
		self.send_response(200)
		self.send_header('queries_received', customRequestHandler._num_queries_received)
		self.end_headers()
		self.wfile.write(self.emit_html_header())
		self.wfile.write("<P>Success!</p>")
		self.wfile.write("<P>Queries received: {0}</p>".format(
				customRequestHandler._num_queries_received))
		self.wfile.write(self.emit_html_footer())
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



# EOF
