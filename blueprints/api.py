import time
from datetime import datetime

from flask import Blueprint, request

import helper
from Forecast import OpenWeatherMapForecasts
from repositories.CityRepository import CityRepository

api = Blueprint('api', __name__)


@api.route('/api/forecast')
def index():
    if 'city_id' not in request.args:
        return {'success': False}

    city_repository = CityRepository()

    city = city_repository.find_city_by_id(request.args.get('city_id'))
    if city is None:
        return {'success': False}
    coords_string = city.coords.replace("{", "")
    coords_string = coords_string.replace("}", "")
    coords_string = coords_string.split(",")
    lon = coords_string[0].split(":")[1].replace(" ", "")
    lat = coords_string[1].split(":")[1].replace(" ", "")
    selection = {'lat': lat, 'lon': lon, 'title': city.city}

    owm_fetcher = OpenWeatherMapForecasts()
    weather = owm_fetcher.get_current_by_lat_lon(selection['lat'], selection['lon'])

    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    utc_diff_in_sec = (weather['timezone'] + offset)
    weather['dt'] = weather['dt'] + utc_diff_in_sec
    weather['dt'] = datetime.fromtimestamp(weather['dt'])

    forecast = owm_fetcher.get_forecast_by_lat_lon(selection['lat'], selection['lon'])

    custom_forecast = {}
    for day in forecast['list']:
        date = datetime.fromtimestamp(day['dt'] + utc_diff_in_sec)
        day['dt'] = str(date)
        day['day_of_the_week'] = helper.day_of_the_week(date.weekday())
        day['main']['temp'] = round(day['main']['temp'])
        day['main']['temp_min'] = round(day['main']['temp_min'])
        day['main']['temp_max'] = round(day['main']['temp_max'])

        if not date.weekday() in custom_forecast:
            custom_forecast[date.weekday()] = []
        temp_style = "background-color: #D3D3D3;"

        if day['main']['temp'] >= 35 and day['main']['temp'] <= 39:
            temp_style = 'background-color: #FFA500;font-weight: bold;'
        if day['main']['temp'] >= 40:
            temp_style = 'background-color: #FF0000;font-weight: bold;'

        custom_forecast[date.weekday()].append({
            'day': day['day_of_the_week'],
            'icon': day['weather'][0]['icon'],
            'date': str(date.date()),
            'time': str(date.time())[:len(str(date.time())) - 3],
            'temp': day['main']['temp'],
            'temp_style': temp_style,
            'humidity': day['main']['humidity'],
            'wind_speed': day['wind']['speed'],
            'feels': day['main']['feels_like'],
            'description': day['weather'][0]['description']
        })

    return {'success': True, 'current_weather': weather, 'forecast': custom_forecast}
