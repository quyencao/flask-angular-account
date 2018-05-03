from flask import Blueprint, jsonify, request
from app import mongo
from flask_bcrypt import Bcrypt
from app.helpers.Token import generate_token, decode_token
from app.helpers.Response import Response

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return Response.make_response({'message': 'You must enter a username and password'}, 400)

    username = data['username']
    password = data['password']
    role = 'normal'

    if 'role' in data:
        role = data['role']

    user = mongo.db.users.find_one({'username': username})

    if user:
        return Response.make_response({'message': 'Username is already used.'}, 400)
    else:
        hash_password = Bcrypt().generate_password_hash(password)

        mongo.db.users.insert_one({
            'username': username,
            'password': hash_password,
            'role': role
        })

        return Response.make_response({'message': 'You registered successfully. Please log in.'}, 200)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        response = jsonify({'message': 'You must enter a username and password'})
        response.status_code = 400

        return response

    username = data['username']
    password = data['password']

    user = mongo.db.users.find_one({'username': username})

    if not user:
        return Response.make_response({'message': 'You must register first.'}, 400)
    else:
        check_password = Bcrypt().check_password_hash(user['password'], password)

        if check_password:
            token = generate_token(str(user['_id']), user['role'])
            return Response.make_response({'token': token}, 200)
        else:
            return Response.make_response({'message': 'Your password is wrong'}, 400)

@auth.route('/token/valid', methods=['POST'])
def checkvalidtoken():
    token = request.get_json()['token']

    decode = decode_token(token)

    if decode is not None:
        data = {
            'valid': True,
            'role': decode['role']
        }
    else:
        data = {
            'valid': False
        }

    return Response.make_response(data, 200)