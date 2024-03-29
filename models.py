from app import db, bcrypt
from flask_login import UserMixin

city_user_table = db.Table(
    'city_user',
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('city_id', db.ForeignKey('city.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    cities = db.relationship('City', secondary=city_user_table, backref='users')

    def set_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class City(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(length=255), nullable=False, unique=False)
    city_state = db.Column(db.String(length=255), nullable=False, unique=False)
    country = db.Column(db.String(length=255), nullable=False, unique=False)
    coords = db.Column(db.String(length=255), nullable=False, unique=False)
    region = db.Column(db.String(length=255), nullable=True, unique=False)
    owm_id = db.Column(db.Integer(), nullable=True, unique=False)




