from __future__ import absolute_import
#
# @file globals.py
# Used to manage our global variables (ick, ick, ick!).
#
# It would be entirely possible to add these values to the Flask.config object,
# however although that would make the code cleaner it would also bind us more
# tightly to the Flask framework.

# Import standard libraries
# (None)

# Import third-party libraries
# (None)

# Import custom libraries
# (None)


# Configuration-related globals
app_handle = None
app_name = None
bind_address = None
minion_address = None
minion_port = None
listen_port = None

# Other 'misc' globals
db_filename = None
storage_handle = None


# EOF