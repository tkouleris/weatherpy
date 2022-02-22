import pycountry
from sqlalchemy import text
from app import app, jsonify, request, make_response, jwt, db
from app.models import City, User
import requests
import datetime
from functools import wraps
from app.helpers import getLoggedInUser


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
    auth = request.authorization
    user = User.query.filter_by(name=auth.username).first()
    if user is None:
        return jsonify({'message': 'user does not exist'}), 400

    if not user.check_password_correction(auth.password):
        return jsonify({'message': 'wrong password'}), 400

    token = jwt.encode({'user': user.name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                       app.config['SECRET_KEY'])
    return jsonify({'token': token})


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
