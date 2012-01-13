import json
import bcrypt
from utils import reverse
from settings import db, BCRYPT_WORK_FACTOR
from werkzeug.exceptions import BadRequest, Conflict
from werkzeug.utils import redirect

@accepts('application/json')
def post(request, **values):
    data = json.loads(request.data)
    if not data['password'] and data['username']:
        raise BadRequest
    if db.users.find_one({'username': data['username']}, fields=[]):
        raise Conflict # 409
    data['password'] = bcrypt.hashpw(data['password'], bcrypt.gensalt(BCRYPT_WORK_FACTOR))
    user = db.users.insert(data)
    return redirect(reverse(user), code=303)
