import re

import pycountry
from sqlalchemy import text
from app import app, jsonify, request, make_response, jwt, db
from app.models import City, User
import requests
import datetime
from functools import wraps
from app.helpers import getLoggedInUser


class RegisterValidator(object):
    def __init__(self, response={}):
        self.response = response

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Password Restriction
    # ------------------------
    # At least 8 chars
    # Contains at least one digit
    # Contains at least one lower alpha char and one upper alpha char
    # Contains at least one char within a set of special chars (@#%$^ etc.)
    # Does not contain space, tab, etc.
    password_regex = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,20}'

    def validate(self):

        error_messages = []
        try:
            email = self.response.get("email", None)
            if not email or not re.fullmatch(self.email_regex, email):
                raise Exception("Error")
        except Exception as e:
            error_messages.append("Email is empty or not valid")

        try:
            email = self.response.get("email", None)
            user_exists = User.query.filter_by(email=email).first()
            if user_exists is not None:
                raise Exception("Error")
        except Exception as e:
            error_messages.append("User with this email exists")

        try:
            username = self.response.get("username", None)
            if not username or len(username) < 5:
                raise Exception("Error")
        except Exception as e:
            error_messages.append("Username empty or less than 5 characters")

        try:
            password = self.response.get("password", None)
            if not password or not re.findall(self.password_regex, password):
                raise Exception("Error")
        except Exception as e:
            error_messages.append("Password empty or not valid")

        return error_messages


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except BaseException as e:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/auth/login', methods=['POST'])
def login():
    auth = request.get_json()

    user = User.query.filter_by(email=auth['email']).first()
    if user is None:
        return jsonify({'message': 'user does not exist'}), 400

    if not user.check_password_correction(auth['password']):
        return jsonify({'message': 'wrong password'}), 400

    token = jwt.encode({'user': user.name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                       app.config['SECRET_KEY'])
    return jsonify({'token': token})


@app.route('/auth/register', methods=["POST"])
def register():
    data = request.get_json()
    validator = RegisterValidator(response=data)
    validation_errors = validator.validate()
    if len(validation_errors) > 0:
        return {"status": "error", "message": validation_errors}, 400

    user_to_be_registered = User(name=data['username'], email=data['email'])
    user_to_be_registered.set_password(data['password'])
    db.session.add(user_to_be_registered)
    db.session.commit()

    registered_user = User.query.filter_by(email=data['email']).first()

    return {"results": {"user": registered_user.id, "message": "user created"}}


@app.route('/forecast/<city_id>')
@token_required
def getForecast(city_id):
    city = City.query.filter_by(id=city_id).first()
    url = "https://api.openweathermap.org/data/2.5/forecast?id=" + str(city.owm_id) + "&appid=" + app.config[
        'OWM_KEY'] + "&units=metric"
    response = requests.get(url)
    weather = response.json()['list']
    city = response.json()['city']['name']
    country = response.json()['city']['country']
    response = []
    for i in range(len(weather)):
        sample = {
            'dt': weather[i]['dt'],
            'temperature': weather[i]['main']['temp'],
            'humidity': weather[i]['main']['humidity'],
            'description': weather[i]['weather'][0]['description'],
            'icon': weather[i]['weather'][0]['icon']}
        response.append(sample)

    return {"results": {"info": {"city": city, "country": country}, "weather": response}}


@app.route('/user/forecasts')
@token_required
def getUserForecasts():
    user = getLoggedInUser()
    forecasts = []
    for city in user.cities:
        url = "https://api.openweathermap.org/data/2.5/forecast?id=" + str(city.owm_id) + "&appid=" + app.config[
            'OWM_KEY'] + "&units=metric"
        response = requests.get(url)
        weather = response.json()['list']
        city = response.json()['city']['name']
        country = response.json()['city']['country']
        response = []
        for i in range(len(weather)):
            sample = {
                'dt': weather[i]['dt'],
                'temperature': weather[i]['main']['temp'],
                'humidity': weather[i]['main']['humidity'],
                'description': weather[i]['weather'][0]['description'],
                'icon': weather[i]['weather'][0]['icon']}
            response.append(sample)
        forecasts.append({"info": {"city": city, "country": country}, "weather": response})

    return {"results": forecasts}


@app.route('/countries')
@token_required
def getAllCountries():
    sql = text('SELECT country FROM city GROUP BY country ORDER BY country ASC')
    result = db.engine.execute(sql)
    cities = [row[0] for row in result]
    countries = []
    for city in cities:
        country = pycountry.countries.get(alpha_2=city)
        if country is None: continue
        countries.append({
            "country_name": country.name,
            "country_abbreviation": city
        })

    return {"results": countries}


@app.route('/city/<country>')
@token_required
def getCountryCities(country):
    filtered = request.args.get('filtered')
    if filtered is None:
        cities = City.query.filter_by(country=country).order_by(City.city)
    else:
        filtered = "%{}%".format(filtered)
        cities = City.query.filter(City.city.like(filtered), City.country == country).all()
    return jsonify(results=[i.serialize for i in cities])


@app.route('/user/city/<city>', methods=['POST', 'DELETE'])
@token_required
def addCityToUser(city):
    if request.method == 'POST':
        user = getLoggedInUser()
        city = City.query.filter_by(id=city).first()
        user.cities.append(city)
        db.session.add(user)
        db.session.commit()
    if request.method == 'DELETE':
        user = getLoggedInUser()
        city = City.query.filter_by(id=city).first()
        user.cities.remove(city)
        db.session.add(user)
        db.session.commit()
    return '', 200
