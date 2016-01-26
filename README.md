# Project Overview

This project as implemented demonstrates a simple ``master/minion'' pair
which implements a fairly trivial microservice but which demonstrates code
layout decisions, asynchronous processing, etc.

## Setup
(Because the master and minion will be talking to each other, you will need
three terminal windows: one for the master, one for the minion, and one to
send queries from.  For brevity I will refer to these as the master, minion,
and command windows.

In the master window, create (and activate) a virtualenv:

		$ cd master
		$ virtualenv ./venv_master
		$ . ./venv_master/scripts/activate

Or, if you're on Windows (this is one of the few commands that will be different):

		> .\\venv_master\\scripts\\activate.bat

Install program dependencies:

		(venv_master) $ python src/setup.py install

Note that this install not just the runtime requirements, but tools used for
development and demonstration as well; this is intentional given the nature
of this project as a "demonstration project".  These groups are called out
in the `setup.py` file and for a production system the dev/demo group could
be removed--although there should also be no harm in letting them be deployed.

Initialize the database (this command can be re-run later to clear any stale
entries):

		(venv_master) $ cd src
		(venv_master) $ python initialize.py

In the minion window, repeat these steps to install the requirements for
the minion:

		$ cd minion
		$ virtualenv ./venv_minion
		$ . ./venv_minion/scripts/activate

(or on Windows):

		> .\\venv_minion\\scripts\\activate.bat

and then continue with installation and initialization:

		(venv_minion) $ python src/setup.py install
		(venv_minion) $ cd src
		(venv_minion) $ python initialize.py

## Usage

To start the master:

		(venv_master) $ python master.py

This will start a listening agent on :8010 (you can configure this in the
`master/config.ini` file).

To get a quick list of the available endpoints, you can query the master
itself using the `httpie` utility that was installed during setup:

		(venv_master) $ http localhost:8010/

At this point, you should also (in the minion window) start the minion so that
the master has something to talk to (this will start a listening agent
on :8020):

		(venv_minion) $ python minion.py

(You can change the port the minion listens on in `minion/config.ini` but if
you do then make sure you also update the corresponding `minion_port` entry in
`master/config.ini` so the master can still reach the minion).

In the command window, navigate to either the master or minion folder (it
doesn't matter which) and activate the virtualenv; in the examples below I
was in the master virtualenv.

After making a query to the system, a UUID will be returned that corresponds
to your request (see `/query/<uuid>` below for details).

## Full Example

Initate a query:

		(venv_master) $ http :8010/ask_a_minion/v1/time
		HTTP/1.0 200 OK
		Content-Length: 155
		Content-Type: text/html; charset=utf-8
		Date: Tue, 26 Jan 2016 07:59:29 GMT
		Server: Werkzeug/0.11.3 Python/2.7.2

		{
			"destination": null,
			"message": null,
			"result": "not_finished",
			"status": "pending",
			"uuid": "0da5e1c5-6011-4c05-ae4b-4f120a3cb7ac"
		}

Lookup the status of that query based on the UUID:

		(venv_master) $ http :8010/ask_a_minion/v1/query/0da5e1c5-6011-4c05-ae4b-4f120a3cb7ac
		HTTP/1.0 200 OK
		Content-Length: 180
		Content-Type: text/html; charset=utf-8
		Date: Tue, 26 Jan 2016 07:59:42 GMT
		Server: Werkzeug/0.11.3 Python/2.7.2

		{
			"destination": null,
			"message": "Tue, 26 Jan 2016 07:59:29 +0000",
			"result": "success",
			"status": "finished",
			"uuid": "0da5e1c5-6011-4c05-ae4b-4f120a3cb7ac"
		}

## API

### /query/&lt;uuid&gt;

Lookup the status of a specific job:

		(venv) $ http localhost:8010/ask_a_minion/v1/query/<uuid>

The response will be a JSON object similar to the following:

	{
		"destination": null,
		"message": null,
		"result": "success",
		"status": "finished",
		"uuid": "43406710-7162-472e-89d7-005d5f639a17"
	}

For convenience, keys are sorted alphabetically.

### /time

Ask the minion what time it is.  An optional delay before answering can be
provided:

		(venv) $ http localhost:8010/ask_a_minion/v1/time
		(venv) $ http localhost:8010/ask_a_minion/v1/time?delay=15

The delay is measured in seconds.

After waiting for any timeout, querying the UUID with `/query/<uuid>` will
return a JSON-formatted string similar to the following:

		{
			"destination": null,
			"message": "Tue, 26 Jan 2016 05:51:23 +0000",
			"result": "success",
			"status": "finished",
			"uuid": "df3f9a32-950d-4044-88f2-36d17698a341"
		}

### /magic8ball

Ask the minion to ask the Magic 8-Ball a question:

		(venv) $ http --verbose --form POST :8010/ask_a_minion/v1/magic8ball delay=5 question="Is this a guaranteed predictor of the future?"

`delay` is optional.  As with `/time`, a UUID is immediately returned which
can be used to query the status of the job.

## Running unit-tests

In either the `/master` or `/minion` folder just run `nosetests` to run tests
and generate a coverage report in the `./cover` folder for that component.

## Notes

We use a simple SQLite database for storage; there is an argument that we
can/should use an ORM like SQLalchemy, but for the sake of keeping the demo
`simple' and not cluttering things up with too many third-party libraries, we
do not do that here.
