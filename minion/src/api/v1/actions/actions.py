from __future__ import absolute_import
#
# @file actions.py
# Define actions and callbacks.
#
# Import standard libraries
import json
import threading
import time

# Import third-party libraries
import requests

# Import custom libraries
import global_vars
import http_status_codes
from api.v1.models import job
import storage


def get_time(a_job, delay):
	try:
		a_job.set_status('pending')
		print "Sending to storage"
		a_job.send_to_storage()
		print "Sleeping for '{}' seconds...".format(delay)
		time.sleep(delay)
		print "Setting status to 'running'"
		a_job.set_status('running')
		print "Setting time to {}".format(time.mktime(time.localtime()))
		a_job.set_message(
				time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
		print "Reading-back message: '{}'".format(a_job.get_message())
		print "Sending to storage"
		a_job.send_to_storage()
		a_job.set_status('finished')
		a_job.set_result('success')
	except Exception as e:
		print "An error occurred!"
		a_job.set_message(str(e))
		a_job.set_status('finished')
		a_job.set_result('error')
	finally:
		print "Sending to storage"
		a_job.send_to_storage()
# End of method get_time() ---------------------------------------------------

# EOF