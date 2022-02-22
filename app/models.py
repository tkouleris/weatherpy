from app import db, bcrypt

city_user_table = db.Table('city_user',
                           db.Column('user_id', db.ForeignKey('users.id')),
                           db.Column('city_id', db.ForeignKey('city.id'))
                           )


class City(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(length=255), nullable=False, unique=False)
    city_state = db.Column(db.String(length=255), nullable=False, unique=False)
    country = db.Column(db.String(length=255), nullable=False, unique=False)
    owm_id = db.Column(db.Integer(), nullable=True, unique=False)

    # users = db.relationship('User', secondary=city_user_table, backref='cities')

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'city': self.city,
            'country': self.country,
            'city_state': self.city_state
            # This is an example how to deal with Many2Many relations
            # 'many2many': self.serialize_many2many
        }

    # @property
    # def serialize_many2many(self):
    #     """
    #    Return object's relations in easily serializable format.
    #    NB! Calls many2many's serialize property.
    #    """
    #     return [item.serialize for item in self.many2many]


class User(db.Model):
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
