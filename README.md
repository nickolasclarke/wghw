# WGHW

## Overview
*Proving competency, one line at time*

This is a Flask-based REST API that serves details on the files and folders 
from a directory of your choosing.

## Getting started
### Requirements:
- [Docker, docker-compose](https://docs.docker.com/compose/install/)
- git

1. `git clone` this repository
2. To run the API, from bash, run: `./run`. It will be served from http://127.0.0.1:5000

## API Endpoints:

- `/`
  - GET: Returns a list of all files and folders in the root directory specified.
    - 200 Success
        - Each item in `results` contains the following fields:
            - `name`: str: resource name
            - `owner`: str: UID of the owner
            - `type`: str: resource type
                - `dir`
                - `file`
            - `size`: str: resource size, in XX
            - `permissions`: str: resource permissions, in octal format
        - Example response:
            ```json
            {   "message": "200",
                "results": [
                    {
                    "name": "<file or directory name>",
                    "owner": "<user_id of owner>",
                    "type": "",
                    "size": "",
                    "permissions":"",
                    }
                ]
            }
            ```
    - 4xx Error Response
        - fields:
            - `code`: str: HTTP status code
            - `error`: str: error name
            - `message`: str: error message
        - Example response:
            ```json
            {
                "code":"404",
                "error": "not found",
                "message": "could not find the specified folder or directory"
            }

- `/<dir>[/<subdir>]`
  - GET: Returns all files and folders in the specified directory
    - 200 Successful response:
        - Each item in `results` contains the following fields:
            - `name`: str: resource name
            - `owner`: str: UID of the owner
            - `type`: str: resource type
            - `size`: str: resource size, in XX
            - `permissions`: str: resource permissions, in octal format
        - Example response:
            ```json
            {   "message": "200",
                "results": [
                    {
                    "name": "bar",
                    "owner": "1",
                    "type": "folder",
                    "size": "230",
                    "permissions":"775",
                    }
                ]
            }
            ```
    - 4xx Error Response
        - fields:
            - `code`: str: HTTP status code
            - `error`: str: error name
            - `message`: str: error message
        - Example response:
            ```json
            {
                "code":"404",
                "error": "not found",
                "message": "could not find the specified folder or directory"
            }
- `/<file>`
  - GET: Returns the contents of the specified file
    - 200 Successful response:
        - Each item in `results` contains the following fields:
            - `name`: str: resource name
            - `owner`: str: UID of the owner
            - `type`: str: resource type
            - `size`: str: resource size, in XX
            - `permissions`: str: resource permissions, in octal format
        - Example response:
            ```json
            {   "message": "200",
                "results": [
                    {
                    "name": "bar",
                    "owner": "1",
                    "type": "folder",
                    "size": "230",
                    "permissions":"775",
                    "content": "string of file content"
                    }
                ]
            }
            ```
    - 4xx Error Response
        - fields:
            - `code`: str: HTTP status code
            - `error`: str: error name
            - `message`: str: error message
        - Example response:
            ```json
            {
                "code":"404",
                "error": "not found",
                "message": "could not find the specified folder or directory"
            }

## Development & Testing
Tests can be be run quickly with `./run_tests`
Tests are handled by pytest, using the testing client provided by Flask. They
are executed within the docker container, using the `docker-compose run`
functionality.

## TODOS
- Edge raises an unhandled 500 exception due to the favicon not being present.
- Additional testing for unresolved endpoints
