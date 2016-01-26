from __future__ import absolute_import
#
# @file job.py
# Define the 'job' views.

# Import standard libraries
# (None)

# Import third-party libraries
import flask
import requests

# Import custom libraries
import global_vars
import http_status_codes
from api.v1.models import job


global_vars.app_handle = flask.Flask('demo')  # @TODO: This initialization needs to happen elsewhere!


# @global_vars.app_handle.route('/debug')
# def debug():
	# message = str(global_vars.app_handle.url_map)
	# message += '\n'
	# message += flask.url_for('lookup_uuid', uuid=1234)
	# return message


def generate_route_string(suffix):
	return '/ask_a_minion/v1{0}'.format(suffix)


# For this simple demo, manually register the root path and a few others to
# display the API quick-reference for.
@global_vars.app_handle.route('/', methods=['GET'])
@global_vars.app_handle.route('/ask_a_minion/', methods=['GET'])
@global_vars.app_handle.route('/ask_a_minion/v1/', methods=['GET'])
def api_help():
	# Generate message that gets displayed if an invalid URL is hit.
	allowed_methods = [
		('get_status', {'uuid': '00000000-00000000-00000000-00000000'}),
		('time', {}),
	]
	# response = flask.url_for('lookup_uuid', **allowed_methods[0][1])
	response_list = []
	for each_method in allowed_methods:
		(function_name, function_args) = each_method
		response_list.append(flask.url_for('{}'.format(function_name), **function_args))
		function_pointer = globals()[function_name]
		# If function has no docstring, getattr('__doc__') returns None...
		docstring = getattr(function_pointer, '__doc__')
		if docstring:
			response_list.append(getattr(function_pointer, '__doc__').strip())
		else:
			response_list.append("(No additional documentation available)")
		response_list.append('')  # Causes a blank line to be added to output
	response = '\n'.join(response_list)
	return response
# End of help() --------------------------------------------------------------


@global_vars.app_handle.route(generate_route_string('/query/<uuid>'), methods=['GET'])
def get_status(uuid=None):
	"""Lookup status of a query based on UUID.
	
	If the job is still running, queries the minion and displays the real-time
	status.
	"""
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
	if 'finished' == lookup_job.get_status():
		# Don't query the minion again.
		return (str(lookup_job.to_json_string()))
	# In progress; query the minion.
	#
	# For security we should use 'https' for our requests; for this demo we'll
	# allow the use of 'http'.
	destination_url = 'http://{address}:{port}{endpoint}'.format(
			address=global_vars.minion_address,
			port=global_vars.minion_port,
			endpoint=generate_route_string('/query/{}'.format(uuid)),
	)
	response = requests.get(destination_url)
	
	# We *could* use response.json() here, but then our Job object would need
	# to have {to|from}_storage() but to_json_string() which would emit text
	# and from_json_blob() which would accept an already-encoded JSON object.
	# Better to keep the importers/exporter symmetric (if redundant).
	updated_job = job.Job.from_json_string(response.text)
	updated_job.send_to_storage()
	return updated_job.to_json_string()
# End of get_status() --------------------------------------------------------


@global_vars.app_handle.route(generate_route_string('/time'), methods=['GET'])
def time():
	"""Query the minion for the current time.
	"""
	# For security we should use 'https' for our requests; for this demo we'll
	# allow the use of 'http'.
	destination_url = 'http://{address}:{port}{endpoint}'.format(
			address=global_vars.minion_address,
			port=global_vars.minion_port,
			endpoint=generate_route_string('/time'),
	)
	a = job.Job()
	a.set_status('pending')
	request = requests.post(
			destination_url,
			data={
				'uuid': a.get_uuid()
			}
	)
	a.send_to_storage()
	return(str(a.to_json_string()))
# End of time() --------------------------------------------------------------


# POST /ask_a_minion/v1/time   JSON: delay=TT (seconds)                 returns UUID, then current time (after delay expires)
# POST /ask_a_minion/v1/magic8ball  JSON: delay=TT (seconds) query=??   returns UUID, then Yes/No/Maybe
# POST /ask_a_minion/v1/


# EOF