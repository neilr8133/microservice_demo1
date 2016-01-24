from __future__ import absolute_import
#
# @file initialize.py
#
#
# Destructively [re]initializes the database.

# Import standard libraries
import ConfigParser

# Import third-party libraries
# (None)

# Import custom libraries
import api
import config
import globals
import storage


def generate_table_definitions():
	"""Return a dictionary of tables and definitions we'll be storing.
	
	This method should be updated with new models or updates to existing ones.
	
	@return Dictionary keyed by table names with value being the table
	        definitions.
	"""
	
	models = [
		# (table name, class name)
		('job', api.v1.models.job.Job),
	]
	return models
# End of generate_table_definitions() ----------------------------------------


def clear_tables(definitions):
	print "Clearing old tables..."
	for each_tuple in definitions:
		storage.delete_table(each_tuple[0])
# End of clear_tables() ------------------------------------------------------


def create_new_tables(definitions):
	for each_tuple in definitions:
		print "Creating table '{0}'".format(each_tuple[0])
		storage.create_table(
				each_tuple[0],
				**each_tuple[1]._get_field_definitions())
# End of create_new_tables() -------------------------------------------------


def main():
	config.parse_options()
	storage.initialize()
	definitions = generate_table_definitions()
	clear_tables(definitions)
	create_new_tables(definitions)
	storage.close()
# End of main() --------------------------------------------------------------


if "__main__" == __name__:
	main()

# EOF