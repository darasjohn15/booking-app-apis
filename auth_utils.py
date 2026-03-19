import jwt
from flask import request, jsonify
from functools import wraps
from helpers import date_helper

SECRET_KEY = "Secret_key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Attach decoded info to request context (or pass into function)
            request.user_id = data['user_id']
            request.user_role = data.get('role')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

def generate_jwt(user_name, role):
    token = jwt.encode({'user_id' : user_name, 'role': role, 'exp' : date_helper.get_token_expiration()}, SECRET_KEY, algorithm="HS256")
    return token