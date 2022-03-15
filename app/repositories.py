from sqlalchemy import text

from app import db
from app.models import City


class CityRepository:

    def __init__(self):
        self.model = City

    def add_city_to_user(self, city, user):
        city = City.query.filter_by(id=city).first()
        user.cities.append(city)
        db.session.add(user)
        db.session.commit()

    def delete_city_from_user(self, city, user):
        city = City.query.filter_by(id=city).first()
        user.cities.remove(city)
        db.session.add(user)
        db.session.commit()

    def get_all_countries(self):
        sql = text('SELECT country FROM city GROUP BY country ORDER BY country ASC')
        result = db.engine.execute(sql)
        return [row[0] for row in result]

    def getCityById(self,city_id):
        return City.query.filter_by(id=city_id).first()