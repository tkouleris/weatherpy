import time
from datetime import datetime, timezone

import pycountry
import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text

from app import db
from helper import page_data

options = Blueprint('options', __name__)


@options.route("/options")
@login_required
def options_page():
    selected_country = 'GR'
    if 'selected_country' in request.args:
        selected_country = request.args.get('selected_country')

    from sqlalchemy import text
    query = "SELECT country FROM city GROUP BY country ORDER BY country"
    sql = text(query)
    result = db.session.execute(sql)
    names = [row[0] for row in result]
    countries = []
    for name in names:
        fullname = pycountry.countries.get(alpha_2=name)
        if fullname is not None:
            countries.append({'short': name, 'fullname': fullname.name})

    query = "SELECT * FROM city WHERE country = '" + selected_country + "'" + " ORDER BY city"
    sql = text(query)
    result = db.session.execute(sql)
    cities = []
    for row in result:
        cities.append(row)

    query = "SELECT * FROM city WHERE id in ( SELECT city_id FROM city_user WHERE user_id = " + str(
        current_user.id) + ")"
    sql = text(query)
    result = db.session.execute(sql)
    selected_cities = []
    for row in result:
        selected_cities.append(row)

    return render_template('options.html',
                           countries=countries,
                           cities=cities,
                           selected_country=selected_country,
                           selected_cities=selected_cities,
                           page_data=page_data()
    )


@options.route("/option", methods=['POST'])
@login_required
def insert_option():
    user_id = current_user.id
    query = "SELECT * FROM city_user WHERE user_id="+str(user_id)
    sql = text(query)
    result = db.session.execute(sql)
    user_cities = []
    for row in result:
        user_cities.append(row)
    if len(user_cities) >= 5:
        return jsonify()

    city_id = request.form.get('city_id')
    query = "INSERT INTO city_user (user_id, city_id) VALUES ( "+str(user_id)+", "+str(city_id)+")"
    sql = text(query)
    db.session.execute(sql)
    db.session.commit()

    return jsonify()

@options.route("/option", methods=['DELETE'])
@login_required
def delete_option():
    city_id = request.form.get('city_id')
    user_id = current_user.id
    query = "DELETE FROM city_user WHERE user_id="+str(user_id)+" AND city_id="+str(city_id)
    sql = text(query)
    db.session.execute(sql)
    db.session.commit()

    return jsonify()
