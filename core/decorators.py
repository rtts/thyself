import bcrypt
from settings import db, BCRYPT_WORK_FACTOR, BCRYPT_REGEX
from functools import wraps
from werkzeug.wrappers import Response
from werkzeug.exceptions import Unauthorized

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

def accepts(mimetype):
    '''
    A decorator that accepts one string argument. If it is equal to the
    Content-Type header sent by the client, the decorated function will be
    executed. Else, a 415 response is returned.
    '''
    
    def decorator(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            if request.headers['Content-Type'] == mimetype:
                return f(request, *args, **kwargs)
            else:
                return Response(status=415) # Unsupported media type
        return wrapper
    return decorator
    