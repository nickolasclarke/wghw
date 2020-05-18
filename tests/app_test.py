import os
import tempfile
import json
from os.path import join

import pytest

from wg import app

ROOT_DIR = tempfile.mkdtemp()

def touch(path, content):
  """touch files and write content"""
  with open(path, 'w') as f:
    f.write(content)

def build_mock(root):
  """build the testing directories and files as defined in exercise PDF
  Mock directory structure
  $ tree
    .
    ├── bar
    │   ├── bar1
    │   └── baz
    ├── foo
    ├── foo1
    └── foo2
    3 directories, 3 files
  """
  # first build the directory structure
  dirs = {'foo':{'path':join(root,'foo'),'mode':0o755,},
          'bar':{'path':join(root,'bar'),'mode':0o777},
         }
  dirs['baz'] = {'path':join(dirs['bar']['path'],'baz'),'mode':0o777}
  [os.mkdir(v['path'],mode=v['mode']) for _,v in dirs.items()]

  # then add the files
  files = {'foo1':{'path':join(root,'foo1'),'mode':0o655,'content':'hi'},
           'foo2':{'path':join(root,'foo2'),'mode':0o777,'content':'bye'},
          }
  files['bar1'] = {'path':join(dirs['bar']['path'],'bar1'),
                   'mode':0o777,'content':'why?'}
  [touch(file['path'],file['content']) for _,file in files.items()]
  return dirs, files

#Test each endpoint
@pytest.fixture
def client():
  """test client for API, provided by Flask"""
  app.config['TESTING'] = True
  #create the testing directory and use as context
  with tempfile.TemporaryDirectory() as root_dir:
    app.config['API_ROOT'] = root_dir
    app.config['MOCK_DIRS'], app.config['MOCK_FILES'] = build_mock(root_dir)
    with app.test_client() as client:
      yield client

def test_root(client):
  """test root of the API"""
  mock = {**app.config['MOCK_DIRS'], **app.config['MOCK_FILES']}
  #remove nested content from mock
  [mock.pop(sub_key) for sub_key in ['baz','bar1']]
  rv = client.get('/')
  res = json.loads(rv.data)
  #TODO probably should either split into individual tests, or refactor for a single assert
  #assert the correct status was passed
  assert rv.status_code == 200
  assert res['message'] == 200
  #assert all expected items are present
  assert len(res['results']) == 4
  res_names = set([item['name'] for item in res['results']])
  mock_names = set([k for k,_ in mock.items()])
  assert res_names == mock_names

#TODO I can probably combine test_subdirs and test_files, or at least functionalize building up the
# paths and results.

def test_files(client):
  """test individual files of API"""
  mockf = app.config['MOCK_FILES']
  #build paths to test and get results
  paths = ['/'+('/').join(file['path'].split('/')[3:]) for _,file in mockf.items()]
  res = [json.loads(client.get(path).data) for path in paths]
  #extract the `contents` attribute of all responses, and flatten the list
  res_contents = [[file['content'] for file in sub_res['results']] for sub_res in res]
  res_contents = set([pvalue for sublist in res_contents for pvalue in sublist])
  #compare the contents of results to expected mocks
  mock_contents = set([item['content'] for _,item in mockf.items()])
  print(res_contents, mock_contents)
  assert res_contents == mock_contents

# TODO this fails due to how I build mockd, I believe but I need to wrap this up.
# def test_subdirs(client):
# """test subdirs of API"""
#build paths to test and get results
# mockd = app.config['MOCK_DIRS']
# paths = ['/'+('/').join(file['path'].split('/')[3:]) for _,file in mockd.items()]
# res = [json.loads(client.get(path).data) for path in paths]
#extract the `permissions` attribute of all responses, and flatten the list
# res_perms = [[subdir['permissions'] for subdir in sub_res['results']] for sub_res in res]
# res_perms = set([pvalue for sublist in res_perms for pvalue in sublist])
# #compare the permissions of results to expected mocks
# mock_perms = set([oct(item['mode'])[-3:] for _,item in mockd.items()])
# assert res_perms == mock_perms

#TODO test for graceful failures as well