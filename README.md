# Project Objective and Document Layout

This project was produced as a ``coding demo/test'' with instructions that it
be made publically-available on a repository site.  Below, we first list the
assignment instructions, and then we follow with the normal project-specific
stuff that one would expect to find in a README.

# Assignment
Create a simple REST API and attempt to show what you consider ``best practices''

## Overview
Create a REST API which has more than 1 API call in the language of your
choice. The API should demonstrate best practices for REST, programming, and
maintainability. The project should have some sort of simplified build
(Makefile/setuptools/Maven/etc..) which makes it easy to build and run the
project. The project can use a database, but if a database is used, it should
be something which is simple to run in a testing environment
(SQLite/HSQLDB/etc...).

## Requirements
1. More than 1 REST API endpoints
2. Demonstrate use of HTTP verbs as they relate to REST
3. At least 1 of the REST endpoints should trigger some business logic inside of the application
4. Unit tests

## Bonus Features
The following, optional, features would demonstrate advanced abilities and improve
consideration for the position:

* Async Processing
* API Documentation (Swagger/RAML/etc…)
* Docker deployment (Create a docker container to run the application)
* Unit Test coverage calculations

# Project Overview

This project as implemented demonstrates a simple ``master/minion'' pair
which implements a fairly trivial microservice but which demonstrates code
layout decisions, asynchronous processing, etc.

## Setup
Create (and activate) a virtualenv:

		$ virtualenv ./venv
		$ . ./venv/scripts/activate

(or, if you're on Windows (this is one of the few commands that will be different)):

		> .\\venv\\scripts\\activate.bat

Install program dependencies:

		(venv) $ python src/setup.py install

Note that this install not just the runtime requirements, but tools used for
development and demonstration as well; this is intentional given the nature
of this project as a "demonstration project".  These groups are called out
in the `setup.py` file and for a production system the dev/demo group could
be removed--although there should also be no harm in letting them be deployed.

Initialize the database (this command can be re-run later to clear any
lingering jobs):

		(venv) $ cd src
		(venv) $ python initialize.py

## Testing

In the top-level folder just run `nosetests`.

## Notes

We use a simple SQLite database for storage; there is an argument that we
can/should use an ORM like SQLalchemy, but for the sake of keeping the demo
`simple' and not cluttering things up with too many third-party libraries, we
do not do that here.
