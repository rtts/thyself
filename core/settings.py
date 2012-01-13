import yaml
import pymongo
import re
from werkzeug.routing import Map, Rule

DB_NAME = "thyself"
BCRYPT_WORK_FACTOR = 5
BCRYPT_REGEX = re.compile(r'^....(..)') # place of work factor in existing hashes

db = pymongo.Connection()[DB_NAME]
rules = []
uris = yaml.load(file('manifest.yaml', 'r'))['uris']
for name in uris:
  for method in uris[name]['methods']:
    rules.append(Rule(uris[name]['path'], methods=[method], endpoint="%s.%s" % (name, method)))
map = Map(rules)
