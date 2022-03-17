from app import db
from app.models import User


def user_repository_factory():
    return UserRepositoryImpl()


class UserRepositoryImpl:

    def __init__(self):
        self.model = User()

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def create(self, data):
        user_to_be_registered = User(name=data['username'], email=data['email'])
        user_to_be_registered.set_password(data['password'])
        db.session.add(user_to_be_registered)
        db.session.commit()
        return self.model.query.filter_by(email=data['email']).first()


class UserRepositoryTest:

    def get_user_by_email(self, email):
        pass

    def create(self, data):
        pass
