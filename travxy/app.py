from flask import Flask, jsonify
from datetime import timedelta
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from travxy.db import db
from flask_jwt_extended import JWTManager
from travxy.resources.user import (UserRegister, User, UserLogin, 
                                    UserList, TokenRefresh)
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
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(message='The token has expired',
                        Error='token_expired'), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(description='Signature verification failed', 
                        error='Invalid token'), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(description='Request does not contain any access token',
                    error='Authorization required'), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_data):
        return jsonify(description='The token is not fresh',
                        error='Fresh token required'), 401

    api.add_resource(Category, '/category/<string:name>')
    api.add_resource(CategoryList, '/categories')
    api.add_resource(Tour, '/tour/<string:name>')
    api.add_resource(TourList, '/tours')
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<user_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserList, '/users')
    api.add_resource(TokenRefresh, '/refresh')

    return app


