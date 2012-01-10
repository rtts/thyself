#!/usr/bin/env python
from werkzeug.routing import Map, Rule
import yaml

# populate map
rules = []
stream = file('manifest.yaml', 'r')
uris = yaml.load(stream)['uris']
for name in uris:
  rules.append(Rule(uris[name]['path'], name))
map = Map(rules)
# it works!
exit()

def dispatch(request):
  map.bind_to_environ(request.environ)
  endpoint, values = adapter.match()
  try:
    eval("%s_%s" % (request.method.lower(), endpoint))
  except:
    pass

def application(environ, start_response):
  request = Request(environ)
  dispatch(request)
  
if __name__ == '__main__':
  from werkzeug.serving import run_simple
  run_simple('localhost', 4000, application)
