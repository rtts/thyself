import yaml
import re
from werkzeug.routing import Map, Rule

DB_NAME = "thyself"
BCRYPT_WORK_FACTOR = '05'
BCRYPT_REGEX = re.compile(r'^....(..)') # place of work factor in existing hashes

uris = yaml.load(file('manifest.yaml', 'r'))['uris']
rule_map = Map(
    [
        Rule(uris[name]['path'], methods=[method], endpoint="%s.%s" % (name, method))
        for name in uris
        for method in uris[name]['methods']
    ])
