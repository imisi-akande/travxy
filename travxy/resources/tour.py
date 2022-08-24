from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from travxy.models.tour import TourModel
from travxy.models.tourist import TouristInfoModel
from travxy.models.category import CategoryModel
from travxy.helpers.pagination import get_paginated_list
from sqlalchemy.orm import joinedload


class Tour(Resource):
    @jwt_required()
    def get(self, tour_id):
        tour = TourModel.find_by_id(tour_id)
        if tour:
            return tour.with_category_json()
        return {'message': 'Tour does not exist'}, 404

    @jwt_required()
    def delete(self, tour_id):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        tour = TourModel.find_by_id(tour_id)
        if tour:
            tour.delete_from_db()
            return{'message': 'Tour deleted succesfully'}, 200
        return {'message': 'Tour does not exist'}, 404

class TourList(Resource):
    @jwt_required()
    def get(self):
        tours = [tour.with_category_json() for tour in TourModel.find_all()]
        return get_paginated_list(tours, '/tours',
                                        start=request.args.get('start', 1),
                                        limit=request.args.get('limit', 20))

class SearchTours(Resource):
    @jwt_required()
    def get(self, search_term):
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)
        if current_user is None:
            return {'message': 'User is not a registered tourist'}, 401

        search_term = search_term.title()
        results = TourModel.query.options(joinedload('details_view')).filter(
                        TourModel.name.like(
                        '%'+search_term+'%')).all()
        if not results:
            return {'message': 'Tour does not exist'}, 400
        tours = [result.with_category_json() for result in results]
        return tours

class AdminForNewTours(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401

        name = request.json.get('name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')

        category_id = request.json.get('category_id')

        if not all([name, location, country, about]):
            return {'message': 'Missing fields required'}, 400
        tour = TourModel(name=name, location=location, country=country,
                        about=about)
        category_instance = CategoryModel.find_by_id(category_id)
        if category_instance is None:
            return {'message': 'Category does not exist for this tour'}, 400
        category_instance.tour_details.append(tour)
        try:
            category_instance.save_to_db()
        except:
            return{'message':
                    'An error occured while trying to insert the tour'}, 500
        return tour.with_category_json(), 201

class AdminForSameCategoryTours(Resource):
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

        if not all([tour_id, name, location, country, about]):
            return {'message': 'Missing fields required'}, 400
        tour = TourModel.find_by_id(tour_id)
        same_category_instance = CategoryModel.query.join(TourModel, 
                                CategoryModel.tour_details).filter(
                                CategoryModel.id==category_id).filter(
                                TourModel.id==tour_id).first()
        if tour is None:
            return {'message': 'Tour does not exist'}
        if same_category_instance:
            tour.tour_id = tour_id
            tour.name = name
            tour.location = location
            tour.country = country
            tour.about = about
            for tour_category in tour.categories_info:
                tour.categories_info.remove(tour_category)
                tour.categories_info.append(same_category_instance)
        try:
            tour.save_to_db()
        except:
            return {'message':
                     'An error occured while trying to update the tour'}, 500
        return tour.json()
