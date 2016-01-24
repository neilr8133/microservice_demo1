from __future__ import absolute_import
#
# @file test_job.py
# Unit tests for api.v1.models.job 

# Import standard libraries
import json

# Import third-party libraries
import nose

# Import custom modules
import src.api.v1.models.job as job


class Test_JobResult(object):
	def __init__(self):
		# Define the list of results we expect to find
		self.result_list = [
			'success',
			'error',
			'abort',
		]
	# End of __init__() ------------------------------------------------------
	
	
	def test_has_expected_num_of_results(self):
		"""JobResult: Verify the number of possible results is what we expect"""
		assert len(job.JobResult._result_names) == len(self.result_list)
	# End of test_has_expected_num_of_results() ------------------------------
	
	
	def test_jobresult_to_str(self):
		"""JobResult: Verify that we recognize the expected job numeric values"""
		def _check_mapping(index, text):
			assert job.JobResult.to_str(index) == text
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_result) in zip(
				range(len(self.result_list)), self.result_list):
			yield _check_mapping, expected_index, expected_result
	# End of test_jobresult_to_str() -----------------------------------------
	
	
	
	def test_jobresult_from_str(self):
		"""JobResult: Verify that the status strings are recognized"""
		def _check_mapping(index, text):
			assert job.JobResult.from_str(text) == index
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_result) in zip(
				range(len(self.result_list)), self.result_list):
			yield _check_mapping, expected_index, expected_result
	# End of test_jobresult_from_str() ---------------------------------------
# End of class Test_JobResult ================================================



class Test_JobStatus(object):
	def __init__(self):
		# Define the list of statuses we expect to find
		self.status_list = [
			'not_started',
			'pending',
			'running',
			'finished',
		]
	# End of __init__() ------------------------------------------------------
	
	
	def test_has_expected_num_of_statuses(self):
		"""JobStatus: Verify the number of possible statuses is what we expect"""
		assert len(job.JobStatus._status_names) == len(self.status_list)
	# End of test_has_expected_num_of_statuses() -----------------------------
	
	
	def test_jobstatus_to_str(self):
		"""JobStatus: Verify that we recognize the expected job status numeric codes"""
		def _check_mapping(index, text):
			assert job.JobStatus.to_str(index) == text
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_status) in zip(
				range(len(self.status_list)), self.status_list):
			yield _check_mapping, expected_index, expected_status
	# End of test_jobstatus_to_str() -----------------------------------------
	
	
	
	def test_jobstatus_from_str(self):
		"""JobStatus: Verify that the status strings are recognized"""
		def _check_mapping(index, text):
			assert job.JobStatus.from_str(text) == index
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_status) in zip(
				range(len(self.status_list)), self.status_list):
			yield _check_mapping, expected_index, expected_status
	# End of Test_JobStatus_To_Str() -----------------------------------------
# End of class Test_JobStatus ================================================



class Test_Job_Model(object):
	@nose.tools.raises(TypeError)
	def test_setstatus_disallows_strings(self):
		"""Job_Model: Verify that _set_status disallows string values"""
		job.Job()._set_status('a')
	# End of test_setstatus_disallows_strings() ------------------------------
	
	
	def test_setstatus_accepts_integers(self):
		"""Job_Model: Verify that _set_status allows (possibly invalid) integer values"""
		one_job = job.Job()
		status_code = 0
		one_job._set_status(status_code)
		assert one_job.get_status() == job.JobStatus.to_str(status_code)
	# End of test_setstatus_accepts_integers() -------------------------------
	
	
	def test_dump_json_of_new_object(self):
		"""Job_Model: Dumping JSON of a newly-created object produces expected format"""
		one_job = job.Job()
		dumped_obj = json.loads(one_job.get_json())
		assert dumped_obj['status'] == 'not_started'
	# End of test_dump_json_of_new_object() ----------------------------------
# End of class Test_Job_Model ================================================

# EOF