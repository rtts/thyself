#!/usr/bin/env python
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import yaml
from httplib import HTTPException
import index

# populate map
rules = []
stream = file('manifest.yaml', 'r')
uris = yaml.load(stream)['uris']
for name in uris:
  for method in uris[name]['methods']:
    rules.append(Rule(uris[name]['path'], methods=[method], endpoint="%s.%s" % (name, method)))
#  rules.append(Rule(uris[name]['path'], endpoint=name))
map = Map(rules)

def dispatch(request):
  adapter = map.bind_to_environ(request.environ)
  try:
    endpoint, values = adapter.match()
    print "calling %s" % endpoint
    print request
    print values
    response = eval("%s(request, **values)" % endpoint)
        #endpoints[endpoint](request, **values)
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
