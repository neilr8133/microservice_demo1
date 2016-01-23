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
# (None)



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
	def __init__(self):
		self._status = JobStatus.from_str('not_started')
		self._uuid = str(uuid.uuid4())
	# End of __init__() ------------------------------------------------------
	
	
	def get_uuid(self):
		return self._uuid
	# End of get_uuid() ------------------------------------------------------
	
	
	def get_status(self):
		return self._status
	# End of get_status() ----------------------------------------------------
# End of class Job ===========================================================

# EOF