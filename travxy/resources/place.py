from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from travxy.models.place import PlaceModel
from travxy.models.category import CategoryModel
from travxy.models.user import UserModel
from travxy.helpers.pagination import get_paginated_list
from sqlalchemy.orm import joinedload


class Place(Resource):
    @jwt_required()
    def get(self, place_id):
        place = PlaceModel.find_by_id(place_id)
        if place:
            return place.with_category_json()
        return {'message': 'Place does not exist'}, 404

class PlaceList(Resource):
    @jwt_required()
    def get(self):
        places = [place.with_category_json() for place in PlaceModel.find_all()]
        return get_paginated_list(places, '/places',
                                        start=request.args.get('start', 1),
                                        limit=request.args.get('limit', 20))

class SearchPlaces(Resource):
    @jwt_required()
    def get(self, search_term):
        search_term = search_term.title()
        results = PlaceModel.query.options(joinedload('details_view')).filter(
                        PlaceModel.name.like(
                        '%'+search_term+'%')).all()
        if not results:
            return {'message': 'Place does not exist'}, 400
        places = [result.with_category_json() for result in results]
        return places

class AdminForPlace(Resource):
    @jwt_required()
    def get(self, place_id):
        user_id = get_jwt_identity()
        current_user = UserModel.query.get(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        place = PlaceModel.find_by_id(place_id)
        if place:
            return place.with_category_json()
        return {'message': 'Place does not exist'}, 404

    @jwt_required()
    def put(self, place_id):
        user_id = get_jwt_identity()
        current_user = UserModel.query.get(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        name = request.json.get('name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')
        category_list = request.json.get('categories')

        place = PlaceModel.find_by_id(place_id)
        if place is None:
            return {'message': 'Place does not exist'}
        if not all([place_id, name, location, country, about, category_list]):
            return {'message': 'Missing fields required'}, 400
        categories_to_be_added = CategoryModel.query.filter(
                                CategoryModel.id.in_(category_list)).all()

        place.place_id = place_id
        place.name = name
        place.location = location
        place.country = country
        place.about = about

        new_categories = list(set(categories_to_be_added) - set(place.categories_info.all()))
        categories_to_be_replaced = list(set(place.categories_info.all()) - set(categories_to_be_added))

        for category in place.categories_info.all():
            if category in categories_to_be_replaced:
                place.categories_info.remove(category)
        place.categories_info.extend(new_categories)

        try:
            place.save_to_db()
        except:
            return {'message':
                     'An error occured while trying to update the place'}, 500
        return place.with_category_json()

    @jwt_required()
    def delete(self, place_id):
        user_id = get_jwt_identity()
        current_user = UserModel.query.get(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        place = PlaceModel.find_by_id(place_id)
        if place:
            place.delete_from_db()
            return{'message': 'Place deleted succesfully'}, 200
        return {'message': 'Place does not exist'}, 404

class AdminForPlaces(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        current_user = UserModel.query.get(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        name = request.json.get('name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')
        category_list = request.json.get('categories')

        if not all([name, location, country, about, category_list]):
            return {'message': 'Missing fields required'}, 400
        category_instances = CategoryModel.query.join(
                                PlaceModel.categories_info).filter(
                                CategoryModel.id.in_(category_list)).all()
        place = PlaceModel(name=name, location=location, country=country,
                        about=about)
        for category_instance in category_instances:
            category_instance.place_details.append(place)
        try:
            category_instance.save_to_db()
        except:
            return{'message':
                    'An error occured while trying to insert the place'}, 500
        return place.with_category_json(), 201

    
