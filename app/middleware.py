from functools import wraps

import jwt
from flask import request, jsonify

from app import app
from app.exceptions import UnauthenticatedException


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            token = request.headers.get('Authorization').replace('Bearer ', '')
            if not token:
                return jsonify({'message': 'missing token'}), 403
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except BaseException as e:
            raise UnauthenticatedException(message="No token. Unauthorized!")

        return f(*args, **kwargs)

    return decorated