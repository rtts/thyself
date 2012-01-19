import db
from utils import members_only, respond, ok, decode
from werkzeug.exceptions import Forbidden

def owner(request, program):
    return request.authorization['username'] == program['owner-name']

def get(request, id):
    '''
    Returns the full representation of a program.
    '''
    program = db.get_or_404('programs', id)
    # TODO: translate set ids to hrefs
    #ids = [ObjectId(x) for x in program['sets']]
    #sets = get_list('sets', {'_id': {'$in': ids}})
    return respond(program)

@members_only
def put(request, id):
    program = db.get_or_404('programs', id)
    if not owner(request, program):
        raise Forbidden
    data = decode(request.data)
    db.update('programs', id, data)
    return ok()

@members_only
def delete(request, id):
    program = db.get_or_404('programs', id)
    if not owner(request, program):
        raise Forbidden
    if db.has_stuff('programs', program):
        raise Conflict
    db.remove('programs', id)
    return ok()
