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


@global_vars.app_handle.route(generate_route_string('/'), methods=['GET'])
def help():
	allowed_methods = [
		('lookup_uuid', {'uuid': '00000000-00000000-00000000-00000000'}),
		('time', {}),
	]
	# response = flask.url_for('lookup_uuid', **allowed_methods[0][1])
	response_list = []
	for each_method in allowed_methods:
		(function_name, function_args) = each_method
		print "Looking up {}".format(function_name)
		print globals()
		response_list.append(flask.url_for('{}'.format(function_name), **function_args))
		function_pointer = locals()[function_name]
		response_list.append(getattr(function_pointer, '__doc__', ''))
	response = '\n'.join(response_list)
	#response = '\n'.join(
	#		[flask.url_for('{}'.format(name), **param) for (name, param) in allowed_methods]
	#)
	return response
# End of help() --------------------------------------------------------------


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
	#return 'User requested to lookup Job ID "{0}"'.format(flask.request.)


@global_vars.app_handle.route(generate_route_string('/time'), methods=['POST'])
def time():
	"""Query the minion for the current time.
	"""
	return "Would query the time on a remote computer."
# End of time() --------------------------------------------------------------


# GET  /ask_a_minion/v1/<UUID>
# POST /ask_a_minion/v1/time   JSON: delay=TT (seconds)                 returns UUID, then current time (after delay expires)
# POST /ask_a_minion/v1/magic8ball  JSON: delay=TT (seconds) query=??   returns UUID, then Yes/No/Maybe
# POST /ask_a_minion/v1/


# EOF