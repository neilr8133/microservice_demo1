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


def initialize():
	globals.storage_handle = sqlite3.connect(globals.db_filename)
# End of initialize() --------------------------------------------------------


def close():
	globals.storage_handle.close()
# End of close() -------------------------------------------------------------


def delete_table(table_name):
	# Warning, insecure!  Would like to use prepared statements, but quick
	# research suggests that dynamic table names are not supported (at least
	# in MySQL: <http://stackoverflow.com/a/9252507>).  So, acknowledging
	# that we would want something better for Production (an ORM?), we'll
	# be a little insecure here.
	cursor = globals.storage_handle.cursor()
	statement = 'DROP TABLE if exists "{0}"'.format(table_name)
	cursor.execute(statement)
# End of delete_table() ------------------------------------------------------


def create_table(table_name, **kwargs):
	# Hackish way to create a database; a strong argument could
	# be made that we should be using SQLAlchemy or some other ORM, but for
	# the sake of keeping the demo 'simple' we'll use this...'mess'.
	#
	# (See the note in delete_table() about why this is insecure.)
	cursor = globals.storage_handle.cursor()
	if len(kwargs) == 0:
		raise ValueError("No table description provided to storage.create_table()")
	column_definitions = ','.join(['{0} {1}'.format(k,v) for k,v in kwargs.items()])
	cursor.execute(
		"CREATE TABLE {0} ({1})".format(table_name, column_definitions))
	globals.storage_handle.commit()
# End of create_table() ------------------------------------------------------


def get_one(table_name, query_field, query_value):
	# Hackish query, etc etc etc.
	cursor = globals.storage_handle.cursor()
	statement = 'SELECT * FROM {0} WHERE ?=?'.format(table_name)
	cursor.execute(statement, query_field, query_value)
	return cursor.fetchone()
# End of get_one() -----------------------------------------------------------


def upsert(table_name, key, key_value, **kwargs):
	# Performs an 'update/insert' operation.
	# See above for why we aren't using prepared statements and therefore this
	# is less safe than we'd like (and should NEVER get near a Production
	# system!)
	if len(kwargs) == 0:
		raise ValueError("No values provided to storage.upsert()")
	values = ','.join(['{0} {1}'.format(k,v) for k,v in kwargs.items()])
	cursor = globals.storage_handle.cursor()
	statement = 'INSERT OR REPLACE INTO "{0}" VALUES ({1})'.format(table_name, values)
	cursor.execute(statement)
	globals.storage_handle.commit()
# End of upsert() ------------------------------------------------------------

# EOF