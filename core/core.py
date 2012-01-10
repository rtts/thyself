from werkzeug.routing import Map, Rule

# populate map
rules = []
stream = file('manifest.yaml', 'r')
dict = yaml.load(stream)
for uri in dict['uris']:
  rules.append(Rule(uri['path'], uri['name']))
map = Map(rules)

def dispatch(request):
  map.bind_to_environ(request.environ)
  endpoint, values = adapter.match()
  try:
    eval("%s_%s" % (request.method.lower(), endpoint))

def application(environ, start_response):
  request = Request(environ)
  dispatch(request)
  
if __name__ == '__main__':
  from werkzeug.serving import run_simple
  run_simple('localhost', 4000, application)
