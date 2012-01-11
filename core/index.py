#!/usr/bin/env python
from werkzeug.wrappers import Response
def get(request, **values):
  response = Response('Hi on index!')
  return response