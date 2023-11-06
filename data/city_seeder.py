import os
import json

from app import app
# from app import db
from models import *

with app.app_context():

    file = os.path.dirname(os.path.realpath(__file__)) + "\\city.list.json"

    f = open(file, encoding="utf8")
    cities = json.load(f)
    data_to_import = []
    for city in cities:
        # single_city = {"city": city['name'], "city_state": city['state'], "country": city['country'],
        #                "owm_id": city['id'], "coords": city['coord']}
        single_city = City(city=city['name'], city_state=city['state'], country=city['country'],
                           owm_id=city['id'], coords=city['coord'])
        db.session.add(single_city)
        db.session.commit()
        # data_to_import.append(single_city)
    f.close()
