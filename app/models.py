from app import db, bcrypt


class City(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(length=255), nullable=False, unique=False)
    city_state = db.Column(db.String(length=255), nullable=False, unique=False)
    country = db.Column(db.String(length=255), nullable=False, unique=False)
    owm_id = db.Column(db.Integer(), nullable=True, unique=False)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hashed = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hashed = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
