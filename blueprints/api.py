import json
import time
from datetime import datetime, timezone

from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for
import requests

import helper
from Forecast import OpenWeatherMapForecasts
from app import app
from helper import page_data
from repositories.CityRepository import CityRepository

api = Blueprint('api', __name__)


@api.route('/api/forecast')
def index():
    if 'city_id' not in request.args:
        return {'success': False}
    # if (current_user.is_authenticated):
    #     return redirect(url_for('dashboard.user_dashboard_page'))
    city_repository = CityRepository()
    # demo_list = {
    #     'athens': {'lat': '37.97945', 'lon': '23.716221', 'title': 'Athens'},
    #     'london': {'lat': '51.50853', 'lon': '-0.12574', 'title': 'London'},
    #     'paris': {'lat': '48.853401', 'lon': '2.3486', 'title': 'Paris'},
    #     'madrid': {'lat': '40.489349', 'lon': '-3.68275', 'title': 'Madrid'},
    #     'milan': {'lat': '45.464272', 'lon': '9.18951', 'title': 'Milan'}
    # }

    # selection = demo_list['athens']
    # if 'city' in request.args and request.args.get('city') in demo_list:
    #     selection = demo_list[request.args.get('city')]
    if 'city_id' in request.args:
        city = city_repository.find_city_by_id(request.args.get('city_id'))
        coords_string = city.coords.replace("{", "")
        coords_string = coords_string.replace("}", "")
        coords_string = coords_string.split(",")
        lon = coords_string[0].split(":")[1].replace(" ", "")
        lat = coords_string[1].split(":")[1].replace(" ", "")
        key = city.city.replace(" ", "_").lower()
        selection = {'lat': lat, 'lon': lon, 'title': city.city}

    title = selection['title']

    owm_fetcher = OpenWeatherMapForecasts()
    weather = owm_fetcher.get_current_by_lat_lon(selection['lat'], selection['lon'])

    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    utc_diff_in_sec = (weather['timezone'] + offset)
    weather['dt'] = weather['dt'] + utc_diff_in_sec
    weather['dt'] = datetime.fromtimestamp(weather['dt'])

    forecast = owm_fetcher.get_forecast_by_lat_lon(selection['lat'], selection['lon'])
    # for day in forecast['list']:
    #     date = datetime.fromtimestamp(day['dt'] + utc_diff_in_sec)
    #     day['dt'] = helper.day_of_the_week(date.weekday())+'  '+str(date)

    custom_forecast = {}
    for day in forecast['list']:
        # print(day)
        date = datetime.fromtimestamp(day['dt'] + utc_diff_in_sec)
        day['dt'] = str(date)
        day['day_of_the_week'] = helper.day_of_the_week(date.weekday())
        day['main']['temp'] = round(day['main']['temp'])
        day['main']['temp_min'] = round(day['main']['temp_min'])
        day['main']['temp_max'] = round(day['main']['temp_max'])
        # if not helper.day_of_the_week(date.weekday()) in custom_forecast:
            # custom_forecast[helper.day_of_the_week(date.weekday())] = []
        if not date.weekday() in custom_forecast:
            custom_forecast[date.weekday()] = []
        temp_style = "background-color: #D3D3D3;"

        if day['main']['temp'] >= 35 and day['main']['temp'] <= 39:
            temp_style = 'background-color: #FFA500;font-weight: bold;'
        if day['main']['temp'] >= 40:
            temp_style = 'background-color: #FF0000;font-weight: bold;'
        # custom_forecast[helper.day_of_the_week(date.weekday())].append({
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


    # attica_cities = city_repository.get_cities_by_region('Attica')
    # theassaloniki_cities = city_repository.get_cities_by_region('Thessaloniki')

    # url = 'http://api.ipstack.com/'+format(request.remote_addr)+'?access_key='+app.config['IPSTACK_KEY']
    # r = requests.get(url)
    # j = json.loads(r.text)
    # lat = j['latitude']
    # lon = j['longitude']

    return { 'success':True, 'current_weather': weather, 'forecast': custom_forecast}