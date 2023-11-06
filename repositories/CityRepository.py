from app import db
from sqlalchemy import text

from models import City


class CityRepository:
    def get_user_selected_cities(self, user_id):
        query = "SELECT city.* FROM city LEFT JOIN city_user ON (city_user.city_id = city.id) WHERE city_user.user_id = " + str(
            user_id)
        sql = text(query)
        result = db.session.execute(sql)
        output = []
        for row in result:
            city = City()
            city.id = row.id
            city.city = row.city
            city.city_state = row.city_state
            city.country = row.country
            city.coords = row.coords
            city.owm_id = row.owm_id
            output.append(city)
        return output

    def get_cities_by_region(self, region):
        return City.query.filter_by(region=region).all()

    def find_city_by_id(self, id):
        return City.query.filter_by(id=id).first()
