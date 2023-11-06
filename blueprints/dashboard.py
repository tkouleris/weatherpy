import json
import time
from datetime import datetime, timezone

import requests
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

import helper
from Forecast import OpenWeatherMapForecasts
from repositories.CityRepository import CityRepository
from app import db
from helper import page_data

dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/dashboard")
@login_required
def user_dashboard_page():
    user_id = current_user.id
    city_repository = CityRepository()
    selected_cities = city_repository.get_user_selected_cities(user_id)

    city_list = {}
    from sqlalchemy import text
    query = "SELECT city.* FROM city LEFT JOIN city_user ON (city_user.city_id = city.id) WHERE city_user.user_id = " + str(
        user_id)
    sql = text(query)
    result = db.session.execute(sql)

    selection = {}
    number_of_cities = 0
    for row in result:
        coords_string = row.coords.replace("{", "")
        coords_string = coords_string.replace("}", "")
        coords_string = coords_string.split(",")
        lon = coords_string[0].split(":")[1].replace(" ", "")
        lat = coords_string[1].split(":")[1].replace(" ", "")
        key = row.city.replace(" ", "_").lower()
        city_list[key] = {'lat': lat, 'lon': lon, 'title': row.city}
        if number_of_cities == 0:
            selection = city_list[key]
            selection['title'] = row.city
        number_of_cities += 1
    if number_of_cities > 0:
        if 'city' in request.args and request.args.get('city') in city_list:
            selection = city_list[request.args.get('city')]

        title = selection['title']

        # from app import app
        # key = app.config['OWM_KEY']
        owm_fetcher = OpenWeatherMapForecasts()
        weather = owm_fetcher.get_current_by_lat_lon(selection['lat'], selection['lon'])

        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        utc_diff_in_sec = (weather['timezone'] + offset)
        weather['dt'] = weather['dt'] + utc_diff_in_sec
        weather['dt'] = datetime.fromtimestamp(weather['dt'])

        forecast = owm_fetcher.get_forecast_by_lat_lon(selection['lat'], selection['lon'])
        custom_forecast = {}
        for day in forecast['list']:
            # print(day)
            date = datetime.fromtimestamp(day['dt'] + utc_diff_in_sec)
            day['dt'] = str(date)
            day['day_of_the_week'] = helper.day_of_the_week(date.weekday())
            day['main']['temp'] = round(day['main']['temp'])
            day['main']['temp_min'] = round(day['main']['temp_min'])
            day['main']['temp_max'] = round(day['main']['temp_max'])
            if not helper.day_of_the_week(date.weekday()) in custom_forecast:
                custom_forecast[helper.day_of_the_week(date.weekday())] = []
            custom_forecast[helper.day_of_the_week(date.weekday())].append({
                'icon': day['weather'][0]['icon'],
                'date': str(date.date()),
                'time': str(date.time())[:len(str(date.time())) - 3],
                'temp': day['main']['temp'],
                'humidity': day['main']['humidity'],
                'wind_speed': day['wind']['speed'],
                'feels': day['main']['feels_like'],
                'description': day['weather'][0]['description']
            })

        return render_template('dashboard.html',
                               title=title,
                               weather=weather,
                               custom_forecast=custom_forecast,
                               city_list=city_list,
                               page_data=page_data()
                               )

    return render_template('dashboard_no_city.html', page_data=page_data())
