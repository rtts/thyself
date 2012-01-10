from users import User
import json

def get():
  user = query(User, query_params)
  return json.dumps(user)
  
def put():

