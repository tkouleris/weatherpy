import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_blueprints():

    from blueprints import demo as demo_blueprint
    app.register_blueprint(demo_blueprint.demo)

    from blueprints import api as api_blueprint
    app.register_blueprint(api_blueprint.api)


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['OWM_KEY'] = os.getenv('OWM_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['IPSTACK_KEY'] = os.getenv('IPSTACK_KEY')
    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

init_blueprints()


if __name__ == '__main__':
    app.run()
