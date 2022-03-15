import pycountry
import requests
from flask import Blueprint, request, jsonify
from sqlalchemy import text

from app import db
from app.exceptions import ResourceNotFoundException
from app.forecast.ForecastFetcher import forecast_fetcher_factory
from app.helpers import getLoggedInUser
from app.middleware import token_required
from app.models import City
from app.repositories import CityRepository

forecast = Blueprint('forecast', __name__)


@forecast.route('/forecast/<city_id>')
@token_required
def getForecast(city_id):
    city = City.query.filter_by(id=city_id).first()
    if city is None:
        raise ResourceNotFoundException("city not found")
    fetcher = forecast_fetcher_factory()
    forecast = fetcher.getForecast(city.owm_id)
    return {"results": forecast}


@forecast.route('/user/forecasts')
@token_required
def getUserForecasts():
    user = getLoggedInUser()
    fetcher = forecast_fetcher_factory()
    forecasts = []
    for city in user.cities:
        forecast = fetcher.getForecast(city.owm_id)
        forecasts.append(forecast)

    return {"results": forecasts}


@forecast.route('/countries')
@token_required
def getAllCountries():
    city_repository = CityRepository()
    cities = city_repository.get_all_countries()
    # sql = text('SELECT country FROM city GROUP BY country ORDER BY country ASC')
    # result = db.engine.execute(sql)
    # cities = [row[0] for row in result]
    countries = []
    for city in cities:
        country = pycountry.countries.get(alpha_2=city)
        if country is None: continue
        countries.append({
            "country_name": country.name,
            "country_abbreviation": city
        })

    return {"results": countries}


@forecast.route('/city/<country>')
@token_required
def getCountryCities(country):
    filtered = request.args.get('filtered')
    if filtered is None:
        cities = City.query.filter_by(country=country).order_by(City.city)
    else:
        filtered = "%{}%".format(filtered)
        cities = City.query.filter(City.city.like(filtered), City.country == country).all()
    return jsonify(results=[i.serialize for i in cities])


@forecast.route('/user/city/<city>', methods=['POST', 'DELETE'])
@token_required
def addCityToUser(city):
    city_repository = CityRepository()
    user = getLoggedInUser()
    if request.method == 'POST':

        city_repository.add_city_to_user(city,user)
        # city = City.query.filter_by(id=city).first()
        # user.cities.append(city)
        # db.session.add(user)
        # db.session.commit()
    if request.method == 'DELETE':
        city_repository.delete_city_from_user(city,user)
        # user = getLoggedInUser()
        # city = City.query.filter_by(id=city).first()
        # user.cities.remove(city)
        # db.session.add(user)
        # db.session.commit()
    return '', 200
