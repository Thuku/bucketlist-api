# Bucketlist-api
[![Build Status](https://travis-ci.org/Thuku/bucketlist-api.svg?branch=develop)](https://travis-ci.org/Thuku/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/Thuku/bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/Thuku/bucketlist-api?branch=develop)

## Getting started.
This APi is built using the Flask micro-framework.

For complete documentation visit.
http://docs.bucketlist19.apiary.io/

It uses token authentication to allow users access various resources.

## Routes:
| EndPoint                      | Public Access |
|-------------------------------|---------------|
| POST /authentication/register | TRUE          |
| POST /authentication/login    | TRUE          |
| POST /bucket                  | FALSE         |
| GET /bucket                   | FALSE         |
| GET /bucket/id                | FALSE         |
| PUT /bucket/id                | FALSE         |
| DELETE /bucket/id             | FALSE         |
| POST /bucket/id/items         | FALSE         |
| GET /bucket/id/items          | FALSE         |
| GET /bucket/id/item/id        | FALSE         |
| PUT /bucket/id/item/id        | FALSE         |
| DELETE /bucket/id/item/id     | FALSE         |

## Using the API.
- Create a virtualenv and clone this repository.
- Pip install the all dependencies in the requirements file:
   
   `pip install -r requirements.txt`
- Create `.env` file and set the following:
   
   `export FLASK_APP=run.py`

    `export ENV="development"`

    `export SECRET_KEY="Your key"`

- To run all tests:

    `nosetests --with-coverage --cover-package=app/`
- To start the application:

    `python manage.py runserver`

- You are now ready to explore the API using postman or curls.
- Remeber to set the authorization token in your headers.