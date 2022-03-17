from flask import current_app
from sqlalchemy import text

from app import db
from app.models import City


def city_repository_factory():
    if current_app.config['ENV'] == 'testing':
        return CityRepositoryTest()
    else:
        return CityRepositoryImpl()


class CityRepositoryImpl:

    def __init__(self):
        self.model = City()

    def add_city_to_user(self, city, user):
        city = self.model.query.filter_by(id=city).first()
        user.cities.append(city)
        db.session.add(user)
        db.session.commit()

    def delete_city_from_user(self, city, user):
        city = self.model.query.filter_by(id=city).first()
        user.cities.remove(city)
        db.session.add(user)
        db.session.commit()

    def get_all_countries(self):
        sql = text('SELECT country FROM city GROUP BY country ORDER BY country ASC')
        result = db.engine.execute(sql)
        return [row[0] for row in result]

    def get_city_by_id(self, city_id):
        return self.model.query.filter_by(id=city_id).first()

    def get_cities_by_country_code(self, country_code):
        return self.model.query.filter_by(country=country_code).order_by(City.city)
        pass

    def get_cities_by_city_name(self,filtered, country):
        filtered = "%{}%".format(filtered)
        return self.model.query.filter(City.city.like(filtered), City.country == country).all()


class CityRepositoryTest:

    def add_city_to_user(self, city, user):
        pass

    def delete_city_from_user(self, city, user):
        pass

    def get_all_countries(self):
        pass

    def get_city_by_id(self, city_id):
        return City()
        pass

    def get_cities_by_country_code(self, country_code):
        pass