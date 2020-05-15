import os
import pwd
import json

from flask import Flask, jsonify
from flask_restful import abort, Resource, Api

ROOT_DIR = '/home/nclarke/winhome/repos/wghw/'
#create an instance of the web server and API
app = Flask(__name__)
api = Api(app)

def success(results):
    res = json.dumps({'message':200, 'results':results})
    return res

def error(error, error_code):
    res = json.dumps({'code':error_code,'error':error})
    return

def metadata(item, type:str) -> dict:
    """TODO"""
    #if dir, assumes a DirEntry iterable
    if type == 'dir':
        stat = item.stat()
        name = item.name
        item_type = 'dir' if item.is_dir() else 'file'
    #if file, assumes a unix-like path
    elif type == 'file':
        stat = os.stat(item)
        name = os.path.split(item)[1]
        item_type = type
    else:
        raise ValueError(f'{item} is not valid')
    res = {
        'name':name,
        'owner':pwd.getpwuid(stat.st_uid).pw_name,
        'type':item_type,
        'size':stat.st_size,#TODO
        'permissions': oct(stat.st_mode)[-3:]#TODO
    }
    return res

def dir_details(path:str) -> list:
    target_dir = os.scandir(path)
    res = [metadata(item,'dir') for item in target_dir]
    return res

def file_contents(path:str) -> dict:
    """TODO"""
    res = metadata(path, 'file')
    with open(path) as f:
        content = f.read()
    res['content'] = content
    return res

#API endpoint logic
class Root(Resource):
    def get(self):
        res = dir_details(ROOT_DIR)
        return res

class RelPath(Resource):
    def get(self,rel_path:str):
        path = os.path.join(ROOT_DIR, rel_path)
        try:
            os.path.exists(path)
        except Exception as error:
            error(f'{path}: error!', 400)
        try:
            if os.path.isdir(path):
                #list the path
                res = success(dir_details(path))
            else:
                os.path.isfile(path)
                #list the contents of the file
                res = success(file_contents(path))
        except Exception as error:
            error(f'{path}: error!', 400)
        return res

def main(root_dir:str, debug: bool=False):
    try:
        isinstance(debug, debug=bool)
    except Exception as error:
        print(f'{error}: unknown error')
    else:
        app.run(debug=debug)

api.add_resource(Root,'/')
api.add_resource(RelPath,'/<path:rel_path>')
if __name__ == '__main__':
    app.run(debug=True)
