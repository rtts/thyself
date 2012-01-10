#!/usr/bin/python
from werkzeug.wrappers import Request, Response
import pymongo
from pymongo import Connection

connection = Connection()
db = connection.test_database
programs = db.programs

#class Programs:

#  def do_GET(self):
#    json = programs.find({'user': self.user})
#    return HttpResponse(json, mimetype="application/json")
    
#def main():
def application(environ, start_response):  
  request = Request(environ)
  if request.args.get('name'):
    programs.insert({'name': request.args.get('name')})
  json = programs.find()
  response = Response(json, mimetype='application/json')
  return response(environ, start_response)

if __name__ == '__main__':
  from werkzeug.serving import run_simple
  run_simple('localhost', 4000, application)    
