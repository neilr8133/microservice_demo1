from __future__ import absolute_import
#
# @file storage.py
# Provides an abstracted interface to the storage system.

# During debugging, it was discovered that using a global variable to store
# a handle to the database did not work because when a Flask view was
# triggered, it raised:
#  ``ProgrammingError: SQLite objects created in a thread can only be used in
#    that same thread.The object was created in thread id 12904 and this is
#    thread id 11856''
#
# Therefore, although VERY sub-optimal, as a quick-and-dirty hack we will
# open and close the database connection on every query.  This is VERY
# inefficient and would not scale, but for a demo program it will be `OK'
# (even though the very act of doing so may cause a person to shed tears
# of shame...)


# Import standard libraries
import sqlite3

# Import third-party libraries
# (None)

# Import custom libraries
import global_vars


def connect(db_filename):
	return sqlite3.connect(db_filename)
# End of connect() -----------------------------------------------------------


def close(db_handle):
	db_handle.close()
	db_handle = None
# End of close() -------------------------------------------------------------


def connect_then_disconnect(func):
	# Decorator: connect, before, then disconnect after.  (See the notes at
	# the top of the file for why this is tolerated.)  This also represents
	# a step backward (and seems contrary to) the point of having connect()
	# accept a filename...that's because it is.
	# @TODO: Fixme so that we don't have to connect/disconnect with every DB operation!
	def wrapper(*args, **kwargs):
		global_vars.storage_handle = connect(global_vars.db_filename)
		# print "Calling {} with args {}".format(func, args, kwargs)
		result = func(*args, **kwargs)
		close(global_vars.storage_handle)
		return result
	return wrapper


@connect_then_disconnect
def delete_table(table_name):
	# Warning, insecure!  Would like to use parameterized statements, but
	# table names cannot be parameterized (at least in MySQL: see
	# <http://stackoverflow.com/a/9252507> and others).  So, acknowledging
	# that we would want something better for Production (an ORM?), we'll
	# be a little insecure here.
	cursor = global_vars.storage_handle.cursor()
	statement = 'DROP TABLE if exists "{0}"'.format(table_name)
	cursor.execute(statement)
# End of delete_table() ------------------------------------------------------


@connect_then_disconnect
def create_table(table_name, *args):
	# Hackish way to create a database; a strong argument could
	# be made that we should be using SQLAlchemy or some other ORM, but for
	# the sake of keeping the demo 'simple' we'll use this...'mess'.
	#
	# (See the note in delete_table() about why this is insecure.)
	cursor = global_vars.storage_handle.cursor()
	if len(args) == 0:
		raise ValueError("No table description provided to storage.create_table()")
	column_definitions = ', '.join(['{0} {1}'.format(column,type) for (column,type) in args])
	statement = "CREATE TABLE {0} ({1})".format(table_name, column_definitions)
	print statement
	cursor.execute(statement)
	global_vars.storage_handle.commit()
# End of create_table() ------------------------------------------------------


@connect_then_disconnect
def get_one(model_class, query_field, query_value):
	# Hackish query, etc etc etc.
	cursor = global_vars.storage_handle.cursor()
	column_names = ','.join([column for (column,type) in model_class._get_field_definitions()])
	statement = 'SELECT {0} FROM {1} WHERE {2}=?'.format(
			column_names,
			model_class.get_table_name(),
			query_field,
	)
	# print statement
	# print query_value
	# The oddity on the next line is because .execute() expects a tuple.
	cursor.execute(statement, (query_value,))
	return cursor.fetchone()
# End of get_one() -----------------------------------------------------------


@connect_then_disconnect
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
	cursor = global_vars.storage_handle.cursor()
	cursor.execute(statement, values)
	global_vars.storage_handle.commit()
# End of upsert() ------------------------------------------------------------

# EOF