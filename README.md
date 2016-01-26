# Project Overview

This project as implemented demonstrates a simple ``master/minion'' pair
which implements a fairly trivial microservice but which demonstrates code
layout decisions, asynchronous processing, etc.

## Setup
(Because the master and minion will be talking to each other, you will need two
terminal windows; for brevity I will refer to these as the master and minion
windows

In the 'master' window, create (and activate) a virtualenv:

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

In the 'minion' window, repeat these steps to install the requirements for
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

At this point, you should also start the minion so that the master has
something to talk to (this will start a listening agent on :8020):

		(venv_minion) $ python minion.py

You can change the port the minion listens on in `minion/config.ini` but if
you do then make sure you also update the corresponding `minion_port` entry in
`master/config.ini`.

### /query/<uuid>

To lookup the status of a query perform:

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

## Running unit-tests

In the top-level folder just run `nosetests`.

## Notes

We use a simple SQLite database for storage; there is an argument that we
can/should use an ORM like SQLalchemy, but for the sake of keeping the demo
`simple' and not cluttering things up with too many third-party libraries, we
do not do that here.
