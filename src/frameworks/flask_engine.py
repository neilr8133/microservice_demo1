from __future__ import absolute_import, print_statement
#
# Flask-based engine
#

# Import standard libraries
# (None)

# Import third-party libraries
from flask import Flask, request

# Import custom libraries
# (None)


class simpleHttpServer(object):
	"""Wrap the Flask engine with the same API as the internal engine."""
	
	# Class-level variables
	_num_queries_received = 0
	_keep_running = True
	
	
	def __init__(self,
	             listen_ip='127.0.0.1',
	             listen_port=8000):
		self._app = Flask('API_demo')
		self._listen_ip = listen_ip
		self._listen_port = listen_port
		self.register_endpoint('/die', simpleHttpServer.stop_server)
	# End of __init__() ------------------------------------------------------
	
	
	def register_endpoint(self, path, function):
		self._app.add_url_rule(path, function.__name__, function)
	# End of register_endpoint() ---------------------------------------------
	
	
	def handle_request(self):
		self._app.run(host=self._listen_ip, port=self._listen_port)
	
	@staticmethod
	def stop_server():
		simpleHttpServer._keep_running = False
		# If not running the in Werkzeug Server this would cause an error.
		# But for purposes of this demo, we'll let this slide.
		# (http://flask.pocoo.org/snippets/67/)
		request.environ.get('werkzeug.server.shutdown')()
		return 'Server shutting down...'
	# End of stop_server() ---------------------------------------------------
	
	@staticmethod
	def set_keep_running(new_status=True):
		simpleHttpServer._keep_running = new_status
	# End of set_keep_running() ----------------------------------------------
	
	
	@staticmethod
	def get_keep_running():
		return simpleHttpServer._keep_running
	# End of get_keep_running() ----------------------------------------------


# EOF
