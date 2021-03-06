from __future__ import absolute_import
#
# @file job.py
# Define the 'job' model.
#
# Import standard libraries
import json
import threading
import time

# Import third-party libraries
import requests

# Import custom libraries
import storage



class JobResult(object):
	# JobResult only refers to jobs that have finished running.
	
	_result_names = [
		'not_finished',  # Hasn't finished yet.
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



class Job(threading.Thread):
	
	# Class-level definitions
	# Identify the attributes that should persist in external storage.
	# (Each definition key must also have get_* and set_* methods.)
	_field_definitions = [
		# (column name, column type, default value)
		('uuid', 'text primary key', None),  # Must be set later.
		('status', 'text', 'not_started'),
		('result', 'text', 'not_finished'),
		('destination', 'text', None),
		('message', 'text', None),
	]
	table_name = 'job'
	
	
	def __init__(self, uuid):
		"""Default constructor.
		
		@param[in] to_be_run is the optional task to be executed when the
		           thread launches.
		"""
		# Initialize all fields to their defaults.
		for tuple in Job._get_default_values():
			setattr(self, tuple[0], tuple[1])
		
		# Now perform custom initalization.
		# (Since this is a unique value per instance, we can't set it in the
		# defaults up above.)
		self.set_uuid(uuid)
	# End of __init__() ------------------------------------------------------
	
	
	@staticmethod
	def get_table_name():
		return Job.table_name
	# End of get_table_name() ------------------------------------------------
	
	
	@staticmethod
	def _get_field_definitions():
		return [(column, type) for (column, type, default) in Job._field_definitions]
	# End of _get_field_definitions() ----------------------------------------
	
	
	@staticmethod
	def _get_default_values():
		return [(column, default) for (column, type, default) in Job._field_definitions]
	# End of _get_default_values() -------------------------------------------
	
	
	@staticmethod
	def from_storage(uuid):
		"""Build a Job object based on an entry in storage.
		
		@param[in] uuid UUID of the stored job to reconstruct.
		@return An instance of Job populated by the specified stored contents.
		"""
		row = storage.get_one(Job, 'uuid', uuid)
		if not row:
			# raise ValueError("UUID '{0}' was not found in storage".format(uuid))
			# Let's be a little more gentle.
			return None
		new_job = Job(uuid)
		for tuple in zip(Job._get_field_definitions(), row):
			# Invoke the 'get_*' method for all keys.
			attribute_name = tuple[0][0]
			attribute_value = tuple[1]
			attribute_setter = getattr(new_job, 'set_{0}'.format(attribute_name))
			
			attribute_setter(attribute_value)
		return new_job
	# End of from_storage() --------------------------------------------------
	
	
	def send_to_storage(self):
		"""Send/update the current object to storage."""
		this_obj = {}
		for tuple in Job._get_field_definitions():
			# Invoke the 'get_*' method for all keys; if the answer is None
			# then we omit it.
			attribute = tuple[0]
			this_obj[attribute] = getattr(self, 'get_{0}'.format(attribute))()
		storage.upsert(Job, **this_obj)
	# End send_to_storage() --------------------------------------------------
	
	
	def get_message(self):
		return self.message
	# End of get_message() ---------------------------------------------------
	
	
	def set_message(self, message):
		self.message = message
	# End of set_message() ---------------------------------------------------
	
	
	def get_uuid(self):
		return self.uuid
	# End of get_uuid() ------------------------------------------------------
	
	
	def set_uuid(self, uuid):
		self.uuid = uuid
	# End of set_uuid() ------------------------------------------------------
	
	
	def get_status(self):
		return self.status
	# End of get_status() ----------------------------------------------------
	
	
	def set_status(self, string):
		self.status = string
	# End of set_status() ----------------------------------------------------
	
	
	def get_result(self):
		return self.result
	# End of get_result_string() ---------------------------------------------
	
	
	def set_result(self, string):
		self.result = string
	# End of set_result_string() ---------------------------------------------
	
	
	def get_destination(self):
		return self.destination
	# End of get_destination() -----------------------------------------------
	
	
	def set_destination(self, target_ip):
		self.destination = target_ip
	# End of set_destination() -----------------------------------------------
	
	
	def to_json(self):
		"""Dump an object to JSON format for reporting to client.
		
		@return A JSON-formatted object.
		"""
		this_obj = {}
		for tuple in Job._get_field_definitions():
			# Invoke the 'get_*' method for all keys
			attribute = tuple[0]
			result = getattr(self, 'get_{0}'.format(attribute))()
			this_obj[attribute] = result
		return json.dumps(
			this_obj,
			sort_keys=True,
			indent=4,
			separators=(',', ': '),
		)
	# End of to_json() ------------------------------------------------------
	
	
	def get_time(self, delay):
		self.set_status('pending')
		self.send_to_storage()
		time.sleep(delay)
		self.set_status('running')
		self.set_message(
				time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
		self.send_to_storage()
		self.set_status('finished')
		self.set_result('success')
		self.send_to_storage()
# End of class Job ===========================================================

# EOF