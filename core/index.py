#!/usr/bin/env python
import yaml
from settings import db, uris
from werkzeug.wrappers import Response

def get(request, **values):
    resp = {'members': []}
    for name in uris:
        resp['members'].append(
            {'name': name,
             'href': uris[name]['path']
            })
    response = Response(yaml.dump(resp), content_type='text/plain')
    return response