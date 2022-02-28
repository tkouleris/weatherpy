from app import app, request, jwt
from app.exceptions import ResourceNotFoundException
from app.models import User


def getLoggedInUser():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    user = User.query.filter_by(name=data['user']).first()
    if user is None:
        raise ResourceNotFoundException(message="User not found")
    return user
