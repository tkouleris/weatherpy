import datetime

import jwt
from flask import Blueprint, request, jsonify

from app import app
from app.auth.validators import RegisterValidator
from app.models import User


authentication = Blueprint('authentication', __name__)


@authentication.route('/auth/login', methods=['POST'])
def login():
    auth = request.get_json()

    user = User.query.filter_by(email=auth['email']).first()
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

    user_to_be_registered = User(name=data['username'], email=data['email'])
    user_to_be_registered.set_password(data['password'])
    db.session.add(user_to_be_registered)
    db.session.commit()

    registered_user = User.query.filter_by(email=data['email']).first()

    return {"results": {"user": registered_user.id, "message": "user created"}}
