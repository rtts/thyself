#!/usr/bin/env python
from settings import uris
from utils import respond

def get(request):
    return respond({'members': [{'name': name, 'href': uris[name]['path']} for name in uris]})

