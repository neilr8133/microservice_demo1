from __future__ import absolute_import
#
# @file job.py
# Define the 'job' model.
#
# Import standard libraries
import json
import uuid

# Import third-party libraries
import requests

# Import custom libraries
import storage



class JobResult(object):
	# JobResult only refers to jobs that have finished running.
	
	_result_names = [
		'success', # No error detected
		'error',   # Some error detected
		'abort',   # Job was aborted by external signal
	]
	
	
	@staticmethod
	def to_str(numeric_value):
		if numeric_value < 0 or numeric_value >= len(JobResult._result_names):
			raise ValueError("Numeric code '{0}' not a valid JobResult".format(numeric_value))
		return JobResult._result_names[numeric_value]
	# End of to_str() --------------------------------------------------------
	
	
	@staticmethod
	def from_str(textual_representation):
		if textual_representation not in JobResult._result_names:
			raise ValueError("JobResult string '{}' not a valid result".format(textual_representation))
		return JobResult._result_names.index(textual_representation)
	# End of from_str() ------------------------------------------------------
# End of class JobResult =====================================================



class JobStatus(object):
	_status_names = [
		'not_started', # Not dispatched.
		'pending',     # Dispatched, but may still be waiting to run on minion.
		'running',     # We queried minion status and found the job running.
		'finished',    # Minion reported execution is done (check JobResult).
	]
	
	
	@staticmethod
	def to_str(numeric_value):
		if numeric_value < 0 or numeric_value >= len(JobStatus._status_names):
			raise ValueError("Numeric code '{0}' not a valid JobStatus".format(numeric_value))
		return JobStatus._status_names[numeric_value]
	# End of to_str() --------------------------------------------------------
	
	
	@staticmethod
	def from_str(textual_representation):
		if textual_representation not in JobStatus._status_names:
			raise ValueError("JobStatus string '{}' not a valid status".format(textual_representation))
		return JobStatus._status_names.index(textual_representation)
	# End of from_str() ------------------------------------------------------
# End of class JobStatus =====================================================



class Job(object):
	
	# Class-level definitions
	# Identify the attributes that should persist in external storage.
	_field_definitions = {
		'status': 'text',
		'uuid': 'text',
		'result': 'text',
		'destination': 'text',
	}
	
	def __init__(self):
		# If more fields are added, remember to update get_json().
		self._status_code = JobStatus.from_str('not_started')
		self._uuid = str(uuid.uuid4())
		self._result = None
		self._destination = None
	# End of __init__() ------------------------------------------------------
	
	
	@staticmethod
	def _get_field_definitions():
		return Job._field_definitions
	# End of _get_table_representation() -------------------------------------
	
	
	def get_uuid(self):
		return self._uuid
	# End of get_uuid() ------------------------------------------------------
	
	
	def get_status(self):
		return JobStatus.to_str(self._status_code)
	# End of get_status() ----------------------------------------------------
	
	
	def _set_status(self, numeric_code):
		if not isinstance(numeric_code, int):
			raise TypeError("Invoked _set_status with type '{0}', expected int".format(type(numeric_code)))
		self._status_code = numeric_code
	# End of get_status() ----------------------------------------------------
	
	
	def get_result(self):
		return self._result
	# End of get_status() ----------------------------------------------------
	
	
	def get_destination(self):
		return self._destination
	# End of get_destination() -----------------------------------------------
	
	
	def set_destination(self, target_ip):
		self._destination = target_ip
	# End of set_destination() -----------------------------------------------
	
	
	def get_json(self):
		this_obj = {
				'status': self.get_status(),
				'uuid': self.get_uuid(),
		}
		if self.get_result():
			this_obj['result'] = self.get_result()
		json_obj = json.dumps(
			this_obj,
			sort_keys=True,
			indent=4,
			separators=(',', ': '),
		)
		return json_obj
	# End of get_json() ------------------------------------------------------
	
	
	def dispatch(self):
		self._set_status(JobStatus.from_str('pending'))
		print "Would dispatch job '{0}' to minion at '{1}'".format(self.get_uuid(), self.get_destination())
# End of class Job ===========================================================

# EOF