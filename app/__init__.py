import os
import jwt
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request, make_response
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['OWM_KEY'] = os.getenv('OWM_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes

# class City(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     city = db.Column(db.String(length=255), nullable=False, unique=False)
#     city_state = db.Column(db.String(length=255), nullable=False, unique=False)
#     country = db.Column(db.String(length=255), nullable=False, unique=False)
#     owm_id = db.Column(db.Integer(), nullable=True, unique=False)
#
#
# @app.route('/<city_id>')
# def hello_world(city_id):  # put application's code here
#     city = City.query.filter_by(id=city_id).first()
#     url = "https://api.openweathermap.org/data/2.5/forecast?id=" + str(city.owm_id) + "&appid=" + app.config[
#         'OWM_KEY'] + "&units=metric"
#     response = requests.get(url)
#     weather = response.json()['list']
#     city = response.json()['city']['name']
#     country = response.json()['city']['country']
#     response = []
#     for i in range(len(weather)):
#         sample = {
#             'dt': weather[i]['dt'],
#             'temperature': weather[i]['main']['temp'],
#             'humidity': weather[i]['main']['humidity'],
#             'description': weather[i]['weather'][0]['description'],
#             'icon': weather[i]['weather'][0]['icon']}
#         response.append(sample)
#
#     return {"results": {"info": {"city": city, "country": country}, "weather": response}}
