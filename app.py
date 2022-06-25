from flask import Flask
from datetime import timedelta
from flask_restful import Api
from flask_jwt import JWT
from travxy.resources.user import UserRegister
from travxy.resources.tour import Tour, TourList

from travxy.security import authenticate, identity
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trav_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)


api.add_resource(Tour, '/tour/<string:name>')
api.add_resource(TourList, '/tour')
api.add_resource(UserRegister, '/register')

from db import db
db.init_app(app)
if __name__ == "__main__":
    app.run(port=5000, debug=True)

