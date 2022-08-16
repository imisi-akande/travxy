from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from travxy.models.tour import TourModel
from travxy.models.tourist import TouristInfoModel
from travxy.helpers.pagination import get_paginated_list
from flask import jsonify

class Tour(Resource):
    @jwt_required()
    def get(self, tour_id):
        tour = TourModel.find_by_id(tour_id)
        if tour:
            return tour.json()
        return {'message': 'Tour does not exist'}, 404

    @jwt_required()
    def delete(self, tour_id):
        tour = TourModel.find_by_id(tour_id)
        if tour:
            tour.delete_from_db()
            return{'message': 'Tour deleted succesfully'}, 200
        return {'message': 'Tour does not exist'}

class TourList(Resource):
    @jwt_required()
    def get(self):
        tours = [tour.json() for tour in TourModel.find_all()]
        return get_paginated_list(tours, '/tours',
                                        start=request.args.get('start', 1),
                                        limit=request.args.get('limit', 20))

class AdminForTour(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401

        name = request.json.get('tour_name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')
        category_id = request.json.get('category_id')

        if not all([name, location, country, about, category_id]):
            return {'message': 'Missing fields required'}, 400
        tour = TourModel(name=name, location=location, country=country,
                            about=about, category_id=category_id)
        try:
            tour.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert the tour'}, 500
        return tour.json(), 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        tour_id = request.json.get('tour_id')
        name = request.json.get('name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')
        category_id = request.json.get('category_id')

        if not all([name, location, country, about, category_id]):
            return {'message': 'Missing fields required'}, 400
        tour = TourModel.find_by_id(tour_id)
        if tour is None:
            return {'message': 'Tour does not exist'}
        else:
           tour.tour_id = tour_id
           tour.name = name
           tour.location = location
           tour.country = country
           tour.about = about
           tour.category_id = category_id
        tour.save_to_db()
        return tour.json()



