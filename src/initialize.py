from __future__ import absolute_import
#
# @file initialize.py
# Destructively [re]initializes the database.
#
# This should be run whenever a model is added or modified.

# Import standard libraries
import ConfigParser

# Import third-party libraries
# (None)

# Import custom libraries
import api
import config
import global_vars
import storage


def generate_model_list():
	"""Return a list of models whose definitions we'll be storing.
	
	This method should be updated when new models are added.
	
	@return List of model classes.
	"""
	
	models = [
		api.v1.models.job.Job,
	]
	return models
# End of generate_model_list() -----------------------------------------------


def clear_tables(model_list):
	print "Clearing old tables..."
	for each_model in model_list:
		storage.delete_table(each_model.get_table_name())
# End of clear_tables() ------------------------------------------------------


def create_new_tables(model_list):
	for each_model in model_list:
		print "Creating table '{0}'".format(each_model.get_table_name())
		storage.create_table(
				each_model.get_table_name(),
				*each_model._get_field_definitions())
# End of create_new_tables() -------------------------------------------------


def main():
	config.parse_options()
	global_vars.storage_handle = storage.connect(global_vars.db_filename)
	model_list = generate_model_list()
	clear_tables(model_list)
	create_new_tables(model_list)
	storage.close(global_vars.storage_handle)
# End of main() --------------------------------------------------------------


if "__main__" == __name__:
	main()

# EOF
