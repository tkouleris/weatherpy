import pycountry
from flask import Blueprint, request, jsonify

from app.exceptions import ResourceNotFoundException
from app.forecast.ForecastFetcher import forecast_fetcher_factory
from app.helpers import getLoggedInUser
from app.middleware import token_required
from app.models import City
# from app.repositories import city_repository_factory
# from app.repositories.city_repository import city_repository_factory
from app.repositories.city_repository import city_repository_factory

forecast = Blueprint('forecast', __name__)


@forecast.route('/forecast/<city_id>')
@token_required
def getForecast(city_id):
    city_repository = city_repository_factory()
    city = city_repository.get_city_by_id(city_id)
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
    city_repository = city_repository_factory()
    cities = city_repository.get_all_countries()
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
def city_user(city):
    city_repository = city_repository_factory()
    user = getLoggedInUser()
    if request.method == 'POST':
        city_repository.add_city_to_user(city, user)
    if request.method == 'DELETE':
        city_repository.delete_city_from_user(city, user)
    return '', 200
