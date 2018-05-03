import jwt
from datetime import datetime, timedelta
from app import app

def generate_token(user_id, user_role):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'iat': datetime.utcnow(),
            'user_id': user_id,
            'role': user_role
        }

        jwt_string = jwt.encode(
            payload,
            app.config.get('SECRET'),
            algorithm='HS256'
        )

        return jwt_string.decode()
    except Exception as e:
        return None


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config.get('SECRET'))
        return {'user_id' : payload['user_id'], 'role': payload['role']}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None