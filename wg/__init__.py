import os
import pwd
import json

from flask import Flask, jsonify
from flask_restful import Resource, Api

ROOT_DIR = '/src/www/app_target'
try:
    os.path.isdir(ROOT_DIR)
except OSError as error:
    raise error
#create an instance of the web server and API
app = Flask(__name__)
app.config['API_ROOT'] = ROOT_DIR
api = Api(app)

def success(results):
  res = {'code':200, 'results':results}
  return res

def make_error(error, error_code):
  res = {'code':error_code,'error':error}
  return res

def metadata(item, type:str) -> dict:
  """Builds a dict containing the metadata of `item`"""
  #if dir, assumes a DirEntry iterable
  if type == 'dir':
    stat = item.stat(follow_symlinks=False)
    name = item.name
    item_type = 'dir' if item.is_dir() else 'file'
  #if file, assumes a unix-like path
  elif type == 'file':
    stat = os.stat(item, follow_symlinks=False)
    name = os.path.split(item)[1]
    item_type = type
  else:
    #TODO fail more gracefully
    raise ValueError(f'{item} is not a valid type, should be `dir` or `file`')
  res = {
        'name':name,
        'owner':pwd.getpwuid(stat.st_uid).pw_name,
        'type':item_type,
        'size':stat.st_size,
        'permissions': oct(stat.st_mode)[-3:]
    }
  return res

def dir_details(path:str) -> list:
  """returns a list of metadata for all items in a given path"""
  target_dir = os.scandir(path)
  meta = lambda item: metadata(item,'dir') if item.is_dir() else metadata(item,'file')
  res = [meta(item) for item in target_dir]
  return res

def file_contents(path:str) -> dict:
  """returns a dict of a file's metadata and content"""
  res = metadata(path, 'file')
  with open(path) as f:
    content = f.read()
  res['content'] = content
  return [res]

#API endpoint logic
class Root(Resource):
  """Return list of items in the root directory"""
  def get(self):
    if not os.path.isdir(app.config['API_ROOT']):
      return make_error('Root directory is not a valid path',404)
    try:
      res = success(dir_details(app.config['API_ROOT']))
    except Exception as err:
      return make_error(err,500)
    return res

class RelPath(Resource):
  """Return details of a /<dir>[/<subdir>] or /<file> request"""
  def get(self,rel_path:str):
    path = os.path.join(app.config['API_ROOT'], rel_path)
    if os.path.exists(path):
      pass
    else:
      return make_error(f'{path}: does not appear to be a valid path', 404)
    if os.path.isdir(path):
      #list the path
      return success(dir_details(path))
    elif os.path.isfile(path):
      #list the contents of the file
      return success(file_contents(path))
    else:
      message = f'{path}: is a valid path, but is not a valid `dir` or `file`'
      return make_error(message, 400)

api.add_resource(Root,'/')
api.add_resource(RelPath,'/<path:rel_path>')

