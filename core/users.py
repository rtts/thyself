import db
import bcrypt
from utils import decode, reverse
from settings import BCRYPT_WORK_FACTOR
from werkzeug.exceptions import BadRequest, Conflict
from werkzeug.utils import redirect

def post(request):
    data = decode(request.data)
    if not (data['password'] and data['username']):
        raise BadRequest
    try:
        db.get_or_404('users', {'username': data['username']}, fields=[])
        raise Conflict #409
    except HTTPException:
        pass
    data['password'] = bcrypt.hashpw(data['password'], bcrypt.gensalt(BCRYPT_WORK_FACTOR))
    user = db.insert('users', data)
    return redirect(reverse(user), code=303)
