from flask import Flask
from datetime import timedelta
from flask_restful import Api
from flask_jwt import JWT
from travxy.user import UserRegister
from travxy.tour import Tour, TourList

from travxy.security import authenticate, identity
app = Flask(__name__)

api = Api(app)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)


api.add_resource(Tour, '/tour/<string:name>')
api.add_resource(TourList, '/tour')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

