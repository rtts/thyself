import pymongo
from settings import DB_NAME
from werkzeug.exceptions import NotFound

c = pymongo.Connection()[DB_NAME]
DESCENDING = pymongo.DESCENDING
ASCENDING  = pymongo.ASCENDING

def get_or_404(collection, spec_or_id, fields=None):
    '''
    Retrieves a user object from the database and returns it.
    If the object is not found, raises a 404.
    '''
    data = c[collection].find_one(spec_or_id, fields=fields)
    if not data:
        raise NotFound
    return data

def get_list(collection, params, fields=None):
    return c[collection].find(params['filters'], fields=fields).limit(params['limit']).skip(params['offset']).sort(params['sortby'], params['sort'])
    
def insert(collection, data):
    return c[collection].insert(data)

def update(collection, spec_or_id, data):
    if not isinstance(spec_or_id, dict):
        spec = {'_id': ObjectId(spec_or_id)}
    else:
        spec = spec_or_id
    c[collection].update(spec, {'$set': data})

def remove(collection, spec_or_id):
    '''
    remove a document from the database
    '''
    c[collection].remove(spec_or_id)

def count(collection, spec_or_id):
    c[collection].find(spec_or_id, fields=[]).count()

def has_stuff(collection, document):
    '''
    Checks if the document still has any associated documents.
    TODO: think about this
    '''
    return True
