from flask import Flask, request
from flask_restful import Resource, Api
from data_helper.tour_data import tours
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
app = Flask(__name__)

api = Api(app)


jwt = JWT(app, authenticate, identity) #auth

class TourList(Resource):

    @jwt_required()
    def get(self):
        return {'tours': tours}, 200

    @jwt_required()
    def post(self, id):
        request_data = request.get_json()
        tour = next(filter(lambda tour:tour['id']==id, tours), None)
        new_tour = {
        'id': request_data['id'],
        'name': request_data['name'],
        'detail': {
            'location': request_data['detail']['location'],
            'departure': request_data['detail']['departure'],
            'experience': request_data['detail']['experience'],
            'cost': request_data['detail']['cost'],
            'duration': request_data['detail']['duration']
        }
        }
        if tour is None:
            tours.append(new_tour)
            return {'tour': new_tour}, 201
        else:
            return {'message': 'Tour id already exists'}



class TourByName(Resource):
    @jwt_required()
    def get(self, name):
        tour = next(filter(lambda tour: tour['name'] == name, tours), None)
        if tour is None:
            return {'message': "Tour does not exist"}, 400
        return tour, 200

class TourDetail(Resource):
    @jwt_required()
    def get(self, name):
        for tour in tours:
            if tour['name'] == name:
                return {'detail':tour['detail']}
        return {'message': "Tour does not exist"}, 400

    @jwt_required()
    def put(self, name):
        request_data = request.get_json()
        tour = next(filter(lambda tour: tour['name']==name, tours), None)
        if tour is None:
            return {'message': 'No tour name match'}, 404
        else:
            new_detail = {
                    'name': request_data['name'],
                    'location': request_data['detail']['location'],
                    'departure': request_data['detail']['departure'],
                    'experience': request_data['detail']['experience'],
                    'cost': request_data['detail']['cost'],
                    'duration': request_data['detail']['duration']
                    }
            tour['detail'].update(new_detail)
            return tour

    @jwt_required()
    def delete(self, id):
        global tours
        tours = list(filter(lambda tour: tour['id'] != id, tours))
        return {'message': "Tour deleted succesfully"}

api.add_resource(TourList, '/tour', '/tour/<int:id>')
api.add_resource(TourByName, '/tour/<string:name>')
api.add_resource(TourDetail, '/tour/<int:id>/detail', '/tour/<string:name>/detail')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

