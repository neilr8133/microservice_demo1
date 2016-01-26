from __future__ import absolute_import
#
# @file actions.py
# Define actions and callbacks.
#
# Import standard libraries
import json
import random
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
		# print "Sending to storage"
		a_job.send_to_storage()
		# print "Sleeping for '{}' seconds...".format(delay)
		time.sleep(delay)
		# print "Setting status to 'running'"
		a_job.set_status('running')
		# print "Setting time to {}".format(time.mktime(time.localtime()))
		a_job.set_message(
				time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
		# print "Reading-back message: '{}'".format(a_job.get_message())
		# print "Sending to storage"
		a_job.send_to_storage()
		a_job.set_status('finished')
		a_job.set_result('success')
	except Exception as e:
		a_job.set_message(str(e))
		a_job.set_status('finished')
		a_job.set_result('error')
	finally:
		# print "Sending to storage"
		a_job.send_to_storage()
# End of method get_time() ---------------------------------------------------


def magic8ball(a_job, question, delay):
	try:
		random.seed()
		a_job.set_status('pending')
		a_job.set_message('Waiting {} seconds before start'.format(delay))
		a_job.send_to_storage()
		print "Magic8ball sleeping for {} seconds".format(delay)
		time.sleep(delay)
		print "Magic8ball finished sleeping"
		a_job.set_status('running')
		answer = random.choice([
			'Reply hazy, ask again later.',
			'If you wish it to be so.',
			"For $5 I'll see what I can do.",
		])
		a_job.set_message('"{0}" {1}'.format(question, answer))
		a_job.set_status('finished')
		a_job.set_result('success')
		a_job.send_to_storage()
	except Exception as e:
		a_job.set_message(str(e))
		a_job.set_status('finished')
		a_job.set_result('error')
# End of magic8ball() --------------------------------------------------------
# EOF