from __future__ import absolute_import
#
# @file job.py
# Define the 'job' views.

# Import standard libraries
import threading

# Import third-party libraries
import flask

# Import custom libraries
import global_vars
import http_status_codes
from api.v1.models import job
from api.v1.actions import actions

global_vars.app_handle = flask.Flask('demo')  # @TODO: This initialization needs to happen elsewhere!


def generate_route_string(suffix):
	return '/ask_a_minion/v1{0}'.format(suffix)


@global_vars.app_handle.route(generate_route_string('/query/<uuid>'), methods=['GET'])
def get_status(uuid):
	"""Lookup status of a query based on UUID.
	
	If the job is still running, queries the minion and displays the real-time
	status.
	"""
	# No validation because it's the job of the master to validate input.
	lookup_job = job.Job.from_storage(uuid)
	return (str(lookup_job.to_json()))
# End of get_status() --------------------------------------------------------


@global_vars.app_handle.route(generate_route_string('/time'), methods=['POST'])
def time():
	"""Query the minion for the current time."""
	new_job = job.Job(flask.request.form['uuid'])
	new_thread = threading.Thread(
			target = actions.get_time,
			args=(new_job, int(flask.request.form['delay'])),
	)
	new_thread.start()  # Launch in a separate thread
	return str(new_job.to_json())
# End of time() --------------------------------------------------------------


@global_vars.app_handle.route(generate_route_string('/magic8ball'), methods=['POST'])
def magic8ball():
	"""Ask the minion to ask a question and shake the Magic 8-Ball."""
	new_job = job.Job(flask.request.form['uuid'])
	new_thread = threading.Thread(
			target = actions.magic8ball,
			args=(
					new_job,
					flask.request.form['question'],
					int(flask.request.form['delay'])
			),
	)
	new_thread.start()  # Launch in a separate thread
	return str(new_job.to_json())
# End of magic8ball() --------------------------------------------------------



# EOF
