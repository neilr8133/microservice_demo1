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


def generate_route_string(suffix):
	return '/ask_a_minion/v1{0}'.format(suffix)


@global_vars.app_handle.route(generate_route_string('/query/<uuid>'), methods=['GET'])
def get_status(uuid):
	"""Lookup status of a query based on UUID.
	
	If the job is still running, queries the minion and displays the real-time
	status.
	"""
	lookup_job = job.Job.from_storage(uuid)
	return (str(lookup_job.to_json()))
# End of get_status() --------------------------------------------------------


@global_vars.app_handle.route(generate_route_string('/time'), methods=['GET'])
def time():
	"""Query the minion for the current time.
	"""
	new_job = job.Job('time')
	new_job.start()  # Launches in a separate thread
	return str(new_job.to_json())
# End of time() --------------------------------------------------------------


# POST /ask_a_minion/v1/time   JSON: delay=TT (seconds)                 returns UUID, then current time (after delay expires)
# POST /ask_a_minion/v1/magic8ball  JSON: delay=TT (seconds) query=??   returns UUID, then Yes/No/Maybe
# POST /ask_a_minion/v1/


# EOF