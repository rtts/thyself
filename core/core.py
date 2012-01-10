#!/usr/bin/env python
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import yaml
from httplib import HTTPException

def index(request, **values):
  return Response('hello to index!')
 
endpoints = {'index': index}

# populate map
rules = []
stream = file('manifest.yaml', 'r')
uris = yaml.load(stream)['uris']
for name in uris:
  rules.append(Rule(uris[name]['path'], endpoint=name))
map = Map(rules)

def dispatch(request):
  adapter = map.bind_to_environ(request.environ)
  try:
    endpoint, values = adapter.match()
    response = endpoints[endpoint](request, **values)
  except HTTPException, e:
    response = e
  return response

@Request.application
def application(request):
  response = dispatch(request)
  return response
 
if __name__ == '__main__':
  from werkzeug.serving import run_simple
  run_simple('localhost', 4000, application)
