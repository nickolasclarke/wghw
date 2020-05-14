# WGHW

Proving competency, one line at time

## Paths:

- `/`
  - GET: Returns a list of all files and folders in the root directory specified.
    - 200 Success
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
                    "name": "<file or directory name>",
                    "owner": "<user_id of owner>",
                    "type": "",
                    "size": "",
                    "permissions":"",
                    }
                ]
            }
            ```
    - Error 4xx Response
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
    - Error 4xx Response
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
    - Error 4xx Response
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

