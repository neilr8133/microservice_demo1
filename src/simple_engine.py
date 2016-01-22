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
	
	# Do not override or extend the __init__() method.
	
	def emit_html_header(self):
		return """
<HTML>
	<HEAD>
		<TITLE>Page demo from builtin engine</TITLE>
	</HEAD>
	<BODY>"""
	# End of emit_html_header() ----------------------------------------------
	
	
	def emit_html_footer(self):
		return """
	</BODY>
</HTML>"""
	# End of emit_html_footer() ----------------------------------------------
	
	
	def do_GET(self):
		customRequestHandler._num_queries_received += 1
		self.send_response(200)
		self.send_header('queries_received', customRequestHandler._num_queries_received)
		self.end_headers()
		self.wfile.write(self.emit_html_header())
		self.wfile.write("<P>Success!</p>\n")
		self.wfile.write("<P>Queries received: {0}</p>\n".format(
				customRequestHandler._num_queries_received))
		response = '(None)'
		if self.path.endswith('/yes'):
			response = 'Yes'
		if self.path.endswith('/no'):
			response = 'No'
		if self.path.endswith('/die'):
			response = '(Server shutdown)'
			simpleHttpServer.set_keep_running(False)
		self.wfile.write("<P>API response: {0}</P>".format(response))
		self.wfile.write(self.emit_html_footer())
	# End of do_GET() --------------------------------------------------------
# End of class customRequestHandler ==========================================



class simpleHttpServer(object):
	
	# Declare some class-level variables
	_keep_running = True
	
	def __init__(self,
	             listen_ip='127.0.0.1',
	             listen_port=8000,
	             server_class=BaseHTTPServer.HTTPServer,
	             handler_class=customRequestHandler):
		self._httpd = server_class((listen_ip, listen_port), handler_class)
	# End of __init__() ------------------------------------------------------
	
	
	def handle_request(self):
		self._httpd.handle_request()
	# End of handle_request() ------------------------------------------------
	
	
	@staticmethod
	def set_keep_running(new_status=True):
		simpleHttpServer._keep_running = new_status
	# End of set_keep_running() ----------------------------------------------
	
	
	@staticmethod
	def get_keep_running():
		return simpleHttpServer._keep_running
	# End of get_keep_running() ----------------------------------------------
# End of class simpleHttp ====================================================

# EOF
