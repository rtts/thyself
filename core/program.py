#!/usr/bin/env python
import yaml
import json
from bson import ObjectId, json_util
from werkzeug.wrappers import Response, Request
from pymongo import ASCENDING, DESCENDING

def get(request, db, uris, **values):
  # handle url values
  program_id = values['id']
  
  # handle query parameters (in request.args)
  
  # retrieve representation from db
  program = db.programs.find_one({'_id': ObjectId(program_id)})

  # create representation
  representation = program # maybe links?
  
  # create a response
  return Response(json.dumps(representation, indent=2, default=json_util.default), content_type='text/plain')

def put(request, db, uris, **values):
  program_id = values['id']
  data = json.loads(request.data, object_hook=json_util.object_hook)
  db.programs.update({'_id': ObjectId(program_id)}, data)
  return Response('edited')
  
def delete(request, db, uris, **values):
  program_id = values['id']
  db.programs.remove({'_id': ObjectId(program_id)})
  # make the right response
  return Response('deleted')
  
if __name__ == "__main__":
  import doctest
  doctest.testmod()