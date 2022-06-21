from flask import Flask
from flask_restful import Api
from data_helper.tour_data import tours
from flask_jwt import JWT
from travxy.user import UserRegister
from travxy.tour import Tour, TourList

from travxy.security import authenticate, identity
app = Flask(__name__)

api = Api(app)
app.secret_key = 'tourism247'


jwt = JWT(app, authenticate, identity) #auth


api.add_resource(Tour, '/tour/<string:name>')
api.add_resource(TourList, '/tour')

#api.add_resource(TourDetail, '/tour/<int:id>/detail', '/tour/<string:name>/detail')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

