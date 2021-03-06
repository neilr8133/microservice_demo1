from __future__ import absolute_import
#
# @file test_job.py
# Unit tests for api.v1.models.job 

# Import standard libraries
import json

# Import third-party libraries
import nose

# Import custom modules
import global_vars
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


class Test_Job_Model_Without_Database(object):
	def setUp(self):
		self.a_job = job.Job()
	# End of setUp() ---------------------------------------------------------
	
	
	def test_set_status_updates_internal_sturcture(self):
		"""Job_Model: set_status updates internal structures"""
		self.a_job.set_status('finished')
		assert 'finished' == self.a_job.status
	# End of test_set_status() -----------------------------------------------
	
	
	def test_get_status_reads_internal_sturcture(self):
		"""Job_Model: set_status updates internal structures"""
		self.a_job.status = 'pending'
		assert 'pending' == self.a_job.get_status()
	# End of test_set_status() -----------------------------------------------
	
	
	def test_set_result_updates_internal_sturcture(self):
		"""Job_Model: set_result updates internal structures"""
		self.a_job.set_result('success')
		assert 'success' == self.a_job.result
	# End of test_set_result() -----------------------------------------------
	
	
	def test_get_result_reads_internal_sturcture(self):
		"""Job_Model: set_result updates internal structures"""
		self.a_job.result = 'failure'
		assert 'failure' == self.a_job.get_result()
	# End of test_set_result() -----------------------------------------------
	
	
	def test_set_message_updates_internal_sturcture(self):
		"""Job_Model: set_message updates internal structures"""
		self.a_job.set_message('my message')
		assert 'my message' == self.a_job.message
	# End of test_set_message() ----------------------------------------------
	
	
	def test_get_message_reads_internal_sturcture(self):
		"""Job_Model: set_message updates internal structures"""
		self.a_job.message = 'another message'
		assert 'another message' == self.a_job.get_message()
	# End of test_set_message() ----------------------------------------------
	
	
	def test_dump_json_of_new_object(self):
		"""Job_Model: Dumping JSON of a newly-created object produces expected format"""
		one_job = job.Job()
		dumped_obj = json.loads(one_job.to_json_string())
		assert dumped_obj['status'] == 'not_started'
	# End of test_dump_json_of_new_object() ----------------------------------
# End of class Test_Job_Model_Without_Database ===============================



class Test_Job_Model_With_Database(object):
	def setUp(self):
		# Initialize temporary storage
		# Because storage has to open/close connection with every access (UGH),
		# we can't use ':memory:' or else we lose the DB after every command..
		# UGH!
		global_vars.db_filename = 'DELETE_ME__unittest.sqlite'
		model_list = initialize.generate_model_list()
		initialize.clear_tables(model_list)
		initialize.create_new_tables(model_list)
	# End of setUp() ---------------------------------------------------------
	
	
	def tearDown(self):
		storage.close(global_vars.storage_handle)
	# End of tearDown() ------------------------------------------------------
	
	
	def test_job_serializes_to_database(self):
		"""Job_Model: object serializes to database system correctly"""
		# Create the simulated job and serialize it to storage.
		new_job = job.Job()
		new_job.send_to_storage()
		# Compare what was stored with the original object.
		stored_row = storage.get_one(job.Job, 'uuid', new_job.get_uuid())
		assert new_job.get_uuid() == stored_row[0]
		assert new_job.get_status() == stored_row[1]
		assert new_job.get_result() == stored_row[2]
		assert new_job.get_destination() == stored_row[3]
	# End of test_job_serializes_to_database() -------------------------------
	
	
	def test_job_reconstituted_from_database(self):
		"""Job_Model: successful reconsitution from database system"""
		new_job = job.Job()
		new_job.send_to_storage()
		reconstituted_job = job.Job.from_storage(new_job.get_uuid())
		assert new_job.get_uuid() == reconstituted_job.get_uuid()
		assert new_job.get_status() == reconstituted_job.get_status()
		assert new_job.get_result() == reconstituted_job.get_result()
		assert new_job.get_destination() == reconstituted_job.get_destination()
	# End of test_job_reconstituted_from_database() --------------------------
# End of class Test_Job_Model ================================================

# EOF
