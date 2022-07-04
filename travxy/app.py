from flask import Flask
from datetime import timedelta
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from travxy.db import db
from flask_jwt_extended import JWTManager
from travxy.resources.user import UserRegister, User, UserLogin, UserList
from travxy.resources.tour import Tour, TourList
from travxy.resources.category import Category, CategoryList
from flask_migrate import Migrate

from travxy.config import app_config
migrate = Migrate()

def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    jwt = JWTManager(app)

    api.add_resource(Category, '/category/<string:name>')
    api.add_resource(CategoryList, '/categories')
    api.add_resource(Tour, '/tour/<string:name>')
    api.add_resource(TourList, '/tours')
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<user_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserList, '/users')

    return app


