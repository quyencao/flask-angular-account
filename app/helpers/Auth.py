from flask import request
from functools import wraps
from app.helpers.Response import Response
from app.helpers.Token import decode_token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response.make_response({'message': 'Unauthorize'}, 401)
        print (request.headers)
        access_token = request.headers.get('Authorization')

        result = decode_token(access_token)

        if result is None:
            return Response.make_response({'message': 'Token invalid'}, 400)

        user_id = result['user_id']
        role = result['role']
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' not in request.headers:
            return Response.make_response({'message': 'Unauthorize'}, 401)

        access_token = request.headers.get('x-access-token')

        result = decode_token(access_token)

        if result is None:
            return Response.make_response({'message': 'Token invalid'}, 400)

        user_id = result['user_id']
        role = result['role']
        if role != 'admin':
            return Response.make_response({'message': 'Unauthorize'}, 401)

        return f(*args, **kwargs)
    return decorated