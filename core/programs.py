#!/usr/bin/env python
import yaml
import json
from settings import db, uris
from decorators import members_only
from werkzeug.wrappers import Response
from pymongo import ASCENDING, DESCENDING

@members_only
def get(request, **values):
  """  
  >>> from werkzeug.test import Client
  >>> from werkzeug.testapp import test_app
  >>> from werkzeug.wrappers import BaseResponse
  >>> c = Client(test_app, BaseResponse)
  >>> resp = c.get('/programs/')
  >>> resp.status_code
  200
  """
  # handle url values
  
  # handle query parameters (in request.args)
  filters = {'public': 'true'} # how should filtering work?
  limit   = int(request.args['limit']) if 'limit' in request.args else 25
  offset  = int(request.args['offset']) if 'offset' in request.args else 0
  sortby  = request.args['sortby'] if 'sortby' in request.args else 'title'
  sort    = request.args['sort'] if 'sort' in request.args else ASCENDING
  
  # retrieve data from db using query parameters and values
  iterator = db.programs.find(filters).limit(limit).skip(offset).sort(sortby, sort)
  
  # create a representation of this data
  representation = {}
  representation['members'] = []
  for program in iterator:
    representation['members'].append({'title': program['title'],
                                      'href': uris['programs']['path'] + str(program['_id'])})
#  'members': [{'title': program['title']} for program in iterator]}
  if offset - limit >= 0:
    representation['previous'] =  "%s?offset=%d" % (uris['programs']['path'], offset - limit)
  
  if offset + limit < db.programs.find(filters).count():
    representation['next'] = "%s?offset=%d" % (uris['programs']['path'], offset + limit)
  
  # create a response
  return Response(json.dumps(representation, indent=2), content_type='text/plain')
  
def post(request, **values):
  print "posting program: %s" % request.data
  data = {}
  if request.headers.get('content-type') == 'application/json':
    data = json.loads(request.data)
  elif request.headers.get('content-type') == 'application/yaml':
    data = yaml.load(request.data)
  else:
    # bad request exception
    pass
  
  # validate data
  
  db.programs.insert(data)
  return Response('added')
  
