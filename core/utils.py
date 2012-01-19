import re
import json
import bcrypt
from settings import uris, BCRYPT_WORK_FACTOR, BCRYPT_REGEX
from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest, Unauthorized
from functools import wraps

id_re = re.compile('<id>')

def reverse(name, *args):
    if name in uris:
        if '<id>' in uris[name]['path']:
            return id_re.sub(args[0], uris[name]['path'])
        return uris[name]['path']
    raise ValueError

def redirect(location, status_code=201):
    '''
    Returns a redirect response without a body
    (for use after POST requests)
    '''
    r = Response(status=status_code)
    r.headers.clear()
    r.headers.add('Location', location)
    return r

def respond(data):
    '''
    Accepts a python dictionary as argument, removes the
    _id key if it exists and return a Response object with
    JSON data.
    (for use after GET requests)
    '''
    try:
        del data['_id']
    except KeyError:
        pass
    r = Response(json.dumps(data))
    r.headers['Content-Type'] = 'text/plain'
    return r

def ok():
    '''
    Returns an empty 200 OK response 
    (for use after PUT and DELETE requests)
    '''
    r = Response()
    r.headers.clear()
    return r

def decode(data):
    '''
    Parses json. Returns python dict or raises exception
    '''
    try:
        return json.loads(data)
    except: # json exceptions are undocumented :-@
        raise BadRequest

def members_only(f):
    '''
    A decorator for functions that get a Request as their first argument,
    and return a Response object.
    
    It authenticates the username and password from the authorization header,
    then executes the decorated function. If authentication fails, the decorated
    function is not executed and a 401 Response object is returned directly.
    
    Yes, this is my first self-written decorator :-)
    '''
    
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.authorization and request.authorization.password:
            username = request.authorization.username
            password = request.authorization.password
            result = db.users.find_one({'username': username}, fields=['password'])
            if result:
                hashed = result['password']

                # straight from http://www.mindrot.org/projects/py-bcrypt/
                if bcrypt.hashpw(password, hashed) == hashed:
                    
                    # rehash with new work factor if necessary
                    if not BCRYPT_REGEX.search(password).group() == BCRYPT_WORK_FACTOR:
                        newpass = bcrypt.hashpw(password, bcrypt.gensalt(BCRYPT_WORK_FACTOR))
                        
                        # a modifier update, see www.mongodb.org/display/DOCS/Updating
                        db.users.update({'username': username}, {'$set': {'password': newpass}})
                    
                    return f(request, *args, **kwargs)

        r = Response(status=401)
        r.www_authenticate.set_basic(realm='Please authenticate thyself')
        return r
    return wrapper
