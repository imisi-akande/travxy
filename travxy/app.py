from flask import Flask, jsonify
from datetime import timedelta
from flask_restful import Api
from travxy.db import db
from flask_jwt_extended import JWTManager
from travxy.resources.user import (UserRegister, User, UserLogin, UserLogout, 
                                    UserList, TokenRefresh)
from travxy.resources.tour import Tour, TourList
from travxy.resources.category import Category, CategoryList
from travxy.resources.tourist import TouristList
from travxy.resources.detail import DetailList
from flask_migrate import Migrate
from travxy.blocklist import BLOCKLIST
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

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        return jti in BLOCKLIST

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

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(description="The token has been revoked.",
                        error='token_revoked'), 401

    api.add_resource(Category, '/category/<string:name>')
    api.add_resource(CategoryList, '/categories')
    api.add_resource(Tour, '/tour/<string:name>')
    api.add_resource(TourList, '/tours')
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<user_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(UserList, '/users')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(TouristList, '/tourists')
    api.add_resource(DetailList, '/details')

    return app


