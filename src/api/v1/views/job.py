from __future__ import absolute_import
#
# @file job.py
# Define the 'job' views.

# Import standard libraries
# (None)

# Import third-party libraries
import flask

# Import custom libraries
from api.v1.models import job
import globals


globals.app_handle = flask.Flask('demo')

@globals.app_handle.route('/debug')
def debug():
	print globals.app_handle.url_map
	return 'Debug info printed to console.'

def generate_route_string(suffix):
	return '/ask_question/v1{0}'.format(suffix)

@globals.app_handle.route(generate_route_string('/'))
def hello():
	return 'Hello, world! "{0}"'.format(__name__)

@globals.app_handle.route(generate_route_string('/yes'))
def yes():
	return 'Yes'

@globals.app_handle.route(generate_route_string('/no'))
def no():
	return 'No'

@globals.app_handle.route(generate_route_string('/<uuid>'), methods=['GET'])
def lookup_uuid(uuid=None):
	if not uuid:
		return (400, 'Invalid UUID')
	#lookup_job = job.Job()
	#return 'User requested to lookup Job ID "{0}"'.format(flask.request.)

#@globals.app_handle.route(generate_route_string('/do'), methods=['POST'])
#def do_something():
	# new_job = job.Job()
	# new_job.dispatch()
	
# GET  /ask_question/v1/<UUID>
# POST /ask_question/v1/shake  JSON: delay=TT (seconds)

# EOF