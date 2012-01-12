import bcrypt
from settings import db
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
                    return f(request, *args, **kwargs)

        r = Response(status=401)
        r.www_authenticate.set_basic(realm='Please authenticate thyself')
        return r
    return wrapper
