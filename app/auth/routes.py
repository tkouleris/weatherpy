import datetime

import jwt
from flask import Blueprint, request, jsonify

from app import app
from app.auth.validators import RegisterValidator
from app.repositories.user_repository import user_repository_factory

authentication = Blueprint('authentication', __name__)


@authentication.route('/auth/login', methods=['POST'])
def login():
    auth = request.get_json()
    user_repository = user_repository_factory()
    user = user_repository.get_user_by_email(auth['email'])

    if user is None:
        return jsonify({'message': 'user does not exist'}), 400

    if not user.check_password_correction(auth['password']):
        return jsonify({'message': 'wrong password'}), 400

    token = jwt.encode({'user': user.name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                       app.config['SECRET_KEY'])
    return jsonify({'token': token})


@authentication.route('/auth/register', methods=["POST"])
def register():
    data = request.get_json()
    validator = RegisterValidator(response=data)
    validation_errors = validator.validate()
    if len(validation_errors) > 0:
        return {"status": "error", "message": validation_errors}, 400
    user_repository = user_repository_factory()
    registered_user = user_repository.create(data)

    return {"results": {"user": registered_user.id, "message": "user created"}}
