from data_helper.user_data import users, username_mapping, userid_mapping
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)