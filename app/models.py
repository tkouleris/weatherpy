from app import db


class City(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(length=255), nullable=False, unique=False)
    city_state = db.Column(db.String(length=255), nullable=False, unique=False)
    country = db.Column(db.String(length=255), nullable=False, unique=False)
    owm_id = db.Column(db.Integer(), nullable=True, unique=False)
