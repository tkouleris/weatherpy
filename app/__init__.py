import os
import jwt
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request, make_response
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy




def create_app(config = None):
    load_dotenv()
    app = Flask(__name__)
    if config == None:
        app.config['ENV'] = 'RUN'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['OWM_KEY'] = os.getenv('OWM_KEY')
    if config == 'testing':
        app.config['ENV'] = config
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'testing'
        app.config['OWM_KEY'] = os.getenv('OWM_KEY')

    return app


app = create_app()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from app.auth.routes import authentication
from app.forecast.routes import forecast

app.register_blueprint(authentication)
app.register_blueprint(forecast)
from app import exception_handler
