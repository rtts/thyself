import db
from utils import members_only, decode, reverse, respond
from settings import uris
from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest
  
def validate(data):
    '''
    Checks if the posted program has the right syntax.
    This probably means checking if the set ids exist and have the right names?
    '''
    # TODO: validate program data
    pass

def get_params(dict):
    return {
        'filters': {'public': True},
        'limit': dict.get('limit', 25),
        'offset': dict.get('offset', 0),
        'sortby': dict.get('sortby', 'date'),
        'sort'  : dict.get('sort', db.DESCENDING)}

def get(request, **values):
    '''
    Returns a part of the list of public programs, with the given filter parameters.
    '''
    params = get_params(request.args)
    offset = params['offset']
    limit  = params['limit']
    representation = {}
    if offset - limit >= 0:
        representation['previous'] = "%s?offset=%d" % (reverse(collection), offset - limit)
    if offset + limit < db.count('programs', params['filters']):
        representation['next'] = "%s?offset=%d" % (reverse(collection), offset + limit)
    iterator = db.get_list('programs', params, fields=['title'])
    representation['members'] = [{'title': program['title'],
        'href': reverse('programs') + str(program['_id'])}
        for program in iterator ]
    return respond(representation)
  
@members_only
def post(request):
    data = decode(request.data)
    try:
        validate(data)
    except:
        raise BadRequest
    program = db.insert('programs', data)
    return redirect(reverse(program), code=201)
