## Description
A Flask application to manipulate monetdb and monetdbd through a user interface. The backend exposes a public API so that users can create and use their own interface.

## Installation
Setting up the environment involves a few simple steps.
First make sure you have pipenv installed on your machine and that the pipenv command can be found in your $PATH.
If you do a user installation, you will need to add the right folder to your PATH variable.
```
  pip3 install --user pipenv
  PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"
  export PATH="$PATH:$PYTHON_BIN_PATH"
  which pipenv
```
Then, follow the steps below in order to activate the virtual environment and start the application.
```
  git clone git@github.com:MonetDBSolutions/flask-monetdb-api.git
  cd flask-monetdb-api
  pipenv install --python <python_path>
  pipenv shell
  ./boot.sh
```
Open your favorite browser and navigate to http://localhost:5000

## Existing Endpoints

### monetdbd

1. `/api/v1/monetdbd/create/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"dbfarm":"mydbfarm"}'  http://localhost:5000/api/v1/monetdbd/create`

2. `/api/v1/monetdbd/start/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"dbfarm":"mydbfarm"}'  http://localhost:5000/api/v1/monetdbd/start`

3. `/api/v1/monetdbd/stop/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"dbfarm":"mydbfarm"}'  http://localhost:5000/api/v1/monetdbd/stop`

4. `/api/v1/monetdbd/get/` [GET]

  Examples: `curl -v "http://localhost:5000/api/v1/monetdbd/get?dbfarm=dbfarm&property=all"`
            `curl -v "http://localhost:5000/api/v1/monetdbd/get?dbfarm=dbfarm&property=control,discovery"`

5. `/api/v1/monetdbd/version/` [GET]

  curl -v "http://localhost:5000/api/v1/monetdbd/version"


### monetdb

1. 1. `/api/v1/monetdb/create/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"databases": ["mydb5"], "options": {"port": 50000}, "arguments": {"pass": "456"}}'  http://localhost:5000/api/v1/monetdb/create`

2. `/api/v1/monetdb/start/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"databases": ["mydb5"], "options": {"port": 50000}, "arguments": {}}'  http://localhost:5000/api/v1/monetdb/start`

3. `/api/v1/monetdb/stop/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"databases": ["mydb5"], "options": {"port": 50000}, "arguments": {"all":true}}'  http://localhost:5000/api/v1/monetdb/stop`

4. `/api/v1/monetdb/kill/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"databases": ["mydb5"], "options": {"port": 50000}, "arguments": {"all":true}}'  http://localhost:5000/api/v1/monetdb/kill`

5. `/api/v1/monetdb/status/` [GET]

  Example: `curl -v "http://localhost:5000/api/v1/monetdb/status?long=true&port=50000"`

6. `/api/v1/monetdb/release/` [POST]

  Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"databases": ["mydb5"], "options": {"port": 50000}, "arguments": {}}'  http://localhost:5000/api/v1/monetdb/release`

7. `/api/v1/monetdb/lock/` [POST]

    Example: `curl -v --header "Content-Type: application/json" --request POST --data '{"databases": ["mydb5"], "options": {"port": 50000}, "arguments": {}}'  http://localhost:5000/api/v1/monetdb/lock`

8. `/api/v1/monetdb/version/` [GET]

    Example: `curl -v http://localhost:5000/api/v1/monetdb/version`
