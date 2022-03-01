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

from app.auth.routes import authentication
from app.forecast.routes import forecast

app.register_blueprint(authentication)
app.register_blueprint(forecast)
from app import exception_handler
