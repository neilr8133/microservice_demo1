from __future__ import absolute_import
#
# @file job.py
# Define the 'job' views.

# Import standard libraries
# (None)

# Import third-party libraries
import flask

# Import custom libraries
import global_vars
import http_status_codes
from api.v1.models import job


global_vars.app_handle = flask.Flask('demo')  # @TODO: This initialization needs to happen elsewhere!


@global_vars.app_handle.route('/debug')
def debug():
	message = str(global_vars.app_handle.url_map)
	message += '\n'
	message += flask.url_for('lookup_uuid', uuid=1234)
	return message


def generate_route_string(suffix):
	return '/ask_a_minion/v1{0}'.format(suffix)



@global_vars.app_handle.route(generate_route_string('/<uuid>'), methods=['GET'])
def lookup_uuid(uuid=None):
	if not uuid:
		return ('Invalid UUID', http_status_codes.BAD_REQUEST)
	lookup_job = job.Job.from_storage(uuid)
	if not lookup_job:
		message_obj = {
			'status': 'not_started',
			'result': 'error',
			'message': "UUID '{0}' not valid".format(uuid)
		}
		return (str(message_obj), http_status_codes.BAD_REQUEST)
		#return (message_obj, http_status_codes.BAD_REQUEST)
	#lookup_job = job.Job()
	#return 'User requested to lookup Job ID "{0}"'.format(flask.request.)

#@global_vars.app_handle.route(generate_route_string('/do'), methods=['POST'])
#def do_something():
	# new_job = job.Job()
	# new_job.dispatch()
	
# GET  /ask_a_minion/v1/<UUID>
# POST /ask_a_minion/v1/time   JSON: delay=TT (seconds)                 returns UUID, then current time (after delay expires)
# POST /ask_a_minion/v1/magic8ball  JSON: delay=TT (seconds) query=??   returns UUID, then Yes/No/Maybe
# POST /ask_a_minion/v1/


# EOF