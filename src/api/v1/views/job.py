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


globals.app = flask.Flask('demo')

@globals.app.route('/')
def hello():
	return 'Hello, world!'


_JOB_CALLBACKS = [
	['/', hello],
]

# EOF