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
2. To run the API, from bash, run: `./run <TARGET DIRECTORY PATH>`. It will be 
served from http://127.0.0.1:5000

## API Endpoints:

- `/`
  - GET: Returns HTTP status `code` and a list of all files and folders in the root directory specified.
    - `code` 200 Success
        - Each item in `results` contains the following fields:
            - `name`: str: resource name
            - `owner`: str: UID of the owner
            - `type`: str: a resource type of the following:
                - `dir`: a directory
                - `file`: a file
            - `size`: str: resource size, in bytes
            - `permissions`: str: resource permissions, in octal format
        - Example response:
            ```json
            {   "code": "200",
                "results": [
                    {
                    "name": "bar",
                    "owner": "1",
                    "type": "dir",
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
        - Example response:
            ```json
            {
                "code":"404",
                "error": "not found",
            }

- `/<dir>[/<subdir>]`
  - same as `/` endpoint
- `/<file>`
  - GET: Returns the contents of the specified file
    - 200 Successful response:
        - Each item in `results` contains the following fields:
            - `name`: str: resource name
            - `owner`: str: UID of the owner
            - `type`: str: a resource type of the following:
                - `dir`: a directory
                - `file`: a file
            - `size`: str: resource size, in bytes
            - `permissions`: str: resource permissions, in octal format
            - `content`: str: a string of the contents of the file
        - Example response:
            ```json
            {   "code": "200",
                "results": [
                    {
                    "name": "baz",
                    "owner": "1",
                    "type": "file",
                    "size": "230",
                    "permissions":"775",
                    "content": "string of file content"
                    }
                ]
            }
            ```
    - Error Response
        - fields:
            - `code`: str: HTTP status code
            - `error`: str: error name
        - Example response:
            ```json
            {
                "code":"404",
                "error": "not found",
            }

### Notes:
WG does not currently follow symlinks
## Development & Testing
Tests can be be run quickly with `./run_tests`.

Tests are handled by [pytest](https://docs.pytest.org/en/latest/), using the 
testing client provided by [Flask](https://flask.palletsprojects.com/en/1.1.x/).
They are executed within the docker container, using the `docker-compose run`
functionality.

## TODOS
- Edge browser raises an unhandled 500 exception due to the favicon not being present.
- Additional testing for unresolved endpoints
- more robust handling of 4xx level codes vs 5xx level codes
- more graceful error handling for any given file or directory errors when
hitting directories
