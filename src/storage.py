from __future__ import absolute_import
#
# @file storage.py
# Provides an abstracted interface to the storage system.

# Import standard libraries
import sqlite3

# Import third-party libraries
# (None)

# Import custom libraries
import globals


def initialize(db_filename):
	return sqlite3.connect(db_filename)
# End of initialize() --------------------------------------------------------


def close(db_handle):
	db_handle.close()
	db_handle = None
# End of close() -------------------------------------------------------------


def delete_table(table_name):
	# Warning, insecure!  Would like to use parameterized statements, but
	# table names cannot be parameterized (at least in MySQL: see
	# <http://stackoverflow.com/a/9252507> and others).  So, acknowledging
	# that we would want something better for Production (an ORM?), we'll
	# be a little insecure here.
	cursor = globals.storage_handle.cursor()
	statement = 'DROP TABLE if exists "{0}"'.format(table_name)
	cursor.execute(statement)
# End of delete_table() ------------------------------------------------------


def create_table(table_name, *args):
	# Hackish way to create a database; a strong argument could
	# be made that we should be using SQLAlchemy or some other ORM, but for
	# the sake of keeping the demo 'simple' we'll use this...'mess'.
	#
	# (See the note in delete_table() about why this is insecure.)
	cursor = globals.storage_handle.cursor()
	if len(args) == 0:
		raise ValueError("No table description provided to storage.create_table()")
	column_definitions = ','.join(['{0} {1}'.format(column,type) for (column,type) in args])
	statement = "CREATE TABLE {0} ({1})".format(table_name, column_definitions)
	print statement
	cursor.execute(statement)
	globals.storage_handle.commit()
# End of create_table() ------------------------------------------------------


def get_one(table_name, query_field, query_value):
	# Hackish query, etc etc etc.
	cursor = globals.storage_handle.cursor()
	statement = 'SELECT * FROM {0} WHERE {1}=?'.format(table_name, query_field)
	# The oddity on the next line is because .execute() expects a tuple.
	cursor.execute(statement, (query_value,))
	return cursor.fetchone()
# End of get_one() -----------------------------------------------------------


def upsert(model_class, **values):
	# Performs an 'update/insert' operation.
	if len(values) == 0:
		raise ValueError("No values provided to storage.upsert()")
	# The clunky code here allows us to use SQL statements with named
	# parameters--without hard-coding anything about the table ahead of time--
	# and get rid of bugs like trying to insert an unquoted None and having
	# SQLite think we want to copy the content of a column named 'None'...
	
	prefix = 'INSERT OR REPLACE INTO "{0}" VALUES '.format(model_class.get_table_name())
	placeholders = ', '.join([':{0}'.format(column) for (column, type) in model_class._get_field_definitions()])
	statement = '{0} ({1})'.format(prefix, placeholders)
	cursor = globals.storage_handle.cursor()
	cursor.execute(statement, values)
	globals.storage_handle.commit()
# End of upsert() ------------------------------------------------------------

# EOF