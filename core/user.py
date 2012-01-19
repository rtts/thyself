import db
from utils import members_only, respond, ok, decode
from werkzeug.exceptions import Forbidden, BadRequest, Conflict

def owner(request, user):
    return request.authorization['username'] == user['username']

@members_only
def get(request, id):
    '''
    Returns information about a specific user id. When a user requests
    his own information, the full representation is returned, otherwise
    only the username is returned.
    '''
    user = db.get_or_404('users', id)
    if not owner(request, user):
        user = {'username': user['username']}
    else:
        del user['password']
    return respond(user)

@members_only
def put(request, id):
    '''
    Updates the user representations with the fields submitted. Omitted
    fields remain the same (db uses an update query). Users are only
    allowed to change their own data.
    '''
    user = db.get_or_404('users', id, fields=['username'])
    if not owner(request, user):
        raise Forbidden
    data = decode(request.data)
    db.update('users', {'username': user['username']}, data)
    return ok()

@members_only
def delete(request, id):
    '''
    Deletes the user from the database. Only allowed to delete yourself.
    What happens to all the user-owned data?
    '''
    user = db.get_or_404('users', id, fields=['username'])
    if not owner(request, user):
        raise Forbidden
    
    if db.has_stuff('users', user):
        raise Conflict
    db.remove('users', id)
    return ok()
