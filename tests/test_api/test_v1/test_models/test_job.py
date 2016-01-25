from __future__ import absolute_import
#
# @file test_job.py
# Unit tests for api.v1.models.job 

# Import standard libraries
import json

# Import third-party libraries
import nose

# Import custom modules
import globals
import initialize
import src.api.v1.models.job as job
import storage


class Test_JobResult(object):
	def __init__(self):
		# Define the list of results we expect to find
		self.result_list = [
			'not_finished',
			'success',
			'error',
			'abort',
		]
	# End of __init__() ------------------------------------------------------
	
	
	def test_has_expected_num_of_results(self):
		"""JobResult: number of possible results is what we expect"""
		assert len(job.JobResult._result_names) == len(self.result_list)
	# End of test_has_expected_num_of_results() ------------------------------
	
	
	def test_jobresult_to_str(self):
		"""JobResult: we recognize the expected job numeric values"""
		def _check_mapping(index, text):
			assert job.JobResult.to_str(index) == text
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_result) in zip(
				range(len(self.result_list)), self.result_list):
			yield _check_mapping, expected_index, expected_result
	# End of test_jobresult_to_str() -----------------------------------------
	
	
	
	def test_jobresult_from_str(self):
		"""JobResult: the status strings are recognized"""
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
		"""JobStatus: number of possible statuses is what we expect"""
		assert len(job.JobStatus._status_names) == len(self.status_list)
	# End of test_has_expected_num_of_statuses() -----------------------------
	
	
	def test_jobstatus_to_str(self):
		"""JobStatus: we recognize the expected job status numeric codes"""
		def _check_mapping(index, text):
			assert job.JobStatus.to_str(index) == text
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_status) in zip(
				range(len(self.status_list)), self.status_list):
			yield _check_mapping, expected_index, expected_status
	# End of test_jobstatus_to_str() -----------------------------------------
	
	
	
	def test_jobstatus_from_str(self):
		"""JobStatus: the status strings are recognized"""
		def _check_mapping(index, text):
			assert job.JobStatus.from_str(text) == index
		# End of helper-function _check_mapping() - - - - - - - - -- - - - - -
		
		for (expected_index, expected_status) in zip(
				range(len(self.status_list)), self.status_list):
			yield _check_mapping, expected_index, expected_status
	# End of Test_JobStatus_To_Str() -----------------------------------------
# End of class Test_JobStatus ================================================



class Test_Job_Model(object):
	def test_dump_json_of_new_object(self):
		"""Job_Model: Dumping JSON of a newly-created object produces expected format"""
		one_job = job.Job()
		dumped_obj = json.loads(one_job.get_json())
		assert dumped_obj['status'] == 'not_started'
	# End of test_dump_json_of_new_object() ----------------------------------
	
	
	def test_job_serializes_to_database(self):
		"""Job_Model: object serializes to database system correctly"""
		# Initialize in-memory storage
		db_filename = ':memory:'
		globals.storage_handle = storage.initialize(db_filename)
		model_list = initialize.generate_model_list()
		initialize.create_new_tables(model_list)
		# Create the simulated job and serialize it to storage.
		new_job = job.Job()
		new_job.send_to_storage()
		# Compare what was stored with the original object.
		stored_row = storage.get_one(new_job.get_table_name(), 'uuid', new_job.get_uuid())
		assert new_job.get_uuid() == stored_row[0]
		assert new_job.get_status() == stored_row[1]
		assert new_job.get_result() == stored_row[2]
		assert new_job.get_destination() == stored_row[3]
		storage.close(globals.storage_handle)
# End of class Test_Job_Model ================================================

# EOF