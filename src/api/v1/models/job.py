from __future__ import absolute_import
#
# @file job.py
# Define the 'job' model.
#
# Import standard libraries
import uuid

# Import third-party libraries
# (None)

# Import custom libraries
import storage



class JobResult(object):
	_result_names = [
		'success',
		'error',
		'abort',
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
		'not_started',
		'pending',
		'running',
		'finished',
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
	# For storage purposes, identify the attributes that should persist.
	_field_definitions = {
		'result': 'text',
		'status': 'text',
		'uuid': 'text',
	}
	
	def __init__(self):
		self._status = JobStatus.from_str('not_started')
		self._uuid = str(uuid.uuid4())
		self._result = JobResult
		self.destination = None
	# End of __init__() ------------------------------------------------------
	
	
	@staticmethod
	def _get_field_definitions():
		return Job._field_definitions
	# End of _get_table_representation() -------------------------------------
	
	
	def get_uuid(self):
		return self._uuid
	# End of get_uuid() ------------------------------------------------------
	
	
	def get_status(self):
		return self._status
	# End of get_status() ----------------------------------------------------
	
	
	def get_destination(self):
		return self.destination
	# End of get_destination() -----------------------------------------------
	
	
	def set_destination(self, target_ip):
		self.destination = target_ip
	# End of set_destination() -----------------------------------------------
	
	
	def dispatch(self):
		print "Would dispatch job '{0}' to minion at '{1}'".format(self.get_uuid(), self.get_destination())
# End of class Job ===========================================================

# EOF