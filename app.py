import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_blueprints():
    from blueprints import auth as auth_blueprint
    app.register_blueprint(auth_blueprint.auth)

    from blueprints import demo as demo_blueprint
    app.register_blueprint(demo_blueprint.demo)

    from blueprints import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint.dashboard)

    from blueprints import options as options_blueprint
    app.register_blueprint(options_blueprint.options)

    from blueprints import api as api_blueprint
    app.register_blueprint(api_blueprint.api)


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['OWM_KEY'] = os.getenv('OWM_KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['IPSTACK_KEY'] = os.getenv('IPSTACK_KEY')

    # app.config['SECRET_KEY'] = 'secret-key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # db.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # from .models import User

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    # with app.app_context():
    #     db.create_all()

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
import models

init_blueprints()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
