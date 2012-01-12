#!/usr/bin/env python
import index, programs, program
from settings import map
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest

@Request.application
def application(request):
    adapter = map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        response = eval(endpoint)(request, **values)
    except HTTPException, e:
        # prevent using werkzeug's responses, they're html!
        response = e.get_response(request.environ)
        response.data = ''
        response.headers.set('Content-Length', 0)
    return response

# run server
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)
