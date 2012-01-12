import yaml
import pymongo
from werkzeug.routing import Map, Rule

DB_NAME = "thyself"
db = pymongo.Connection()[DB_NAME]

rules = []
stream = file('manifest.yaml', 'r')
uris = yaml.load(stream)['uris']
for name in uris:
  for method in uris[name]['methods']:
    rules.append(Rule(uris[name]['path'], methods=[method], endpoint="%s.%s" % (name, method)))
map = Map(rules)
