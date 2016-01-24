from __future__ import absolute_import
#
# @file test_job.py
# Unit tests for api.v1.models.job 

# Import standard libraries
# (None)

# Import third-party libraries
import nose

# Import custom modules
import src.api.v1.models.job as job


class test_jobstatus_to_str(object):
	def __init__(self):
		# Define the list of statuses we expect to find
		self.status_list = [
			'not_started',
			'pending',
			'running',
			'finished',
		]
	# End of setUp() ---------------------------------------------------------
	
	
	def test_has_expected_num_of_statuses(self):
		"""Verify the number of possible statuses is what we expect"""
		assert len(job.JobStatus._status_names) == len(self.status_list)
	# End of test_has_expected_num_of_statuses() -----------------------------
	
	
	def test_jobstatus_to_str(self):
		"""Verify that we recognize the expected job status results"""
		def _check_mapping(index, text):
			assert job.JobStatus.to_str(index) == text
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_status) in zip(
				range(len(self.status_list)), self.status_list):
			yield _check_mapping, expected_index, expected_status
	# End of test_jobstatus_to_str() -----------------------------------------
	
	
	
	def test_jobstatus_from_str(self):
		"""Verify that the status strings are what we expect"""
		def _check_mapping(index, text):
			assert job.JobStatus.from_str(text) == index
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_status) in zip(
				range(len(self.status_list)), self.status_list):
			yield _check_mapping, expected_index, expected_status
	# End of test_jobstatus_from_str() ---------------------------------------
# EOF