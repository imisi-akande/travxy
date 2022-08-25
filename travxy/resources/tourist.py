from travxy.models.tourist import TouristInfoModel
from travxy.models.tour import TourModel
from travxy.models.user import UserModel
from travxy.models.detail import DetailModel
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

class Tourist(Resource):
    @jwt_required()
    def get(self, tourist_id):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user is None:
            return {'message': 'User must be a registered tourist'}
        tourist = TouristInfoModel.query.get(tourist_id)
        if tourist is None or tourist.user.isactive == False:
            return {'message': 'tourist does not exist'}, 404
        return tourist.json_with_user_name()

class TouristList(Resource):
    @jwt_required()
    def get(self):
        tourists = TouristInfoModel.query.join(UserModel,
                                                TouristInfoModel.user).filter(
                                                UserModel.isactive==True).all()
        return {'tourists': [tourist.json_with_user_name()
                            for tourist in tourists]}

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if TouristInfoModel.find_by_user_id(user_id):
            return {'message':
                "A tourist with userid '{}' already exists".format(user_id)}, 400

        nationality = request.json.get('nationality')
        gender = request.json.get('gender', 'Neutral')
        if not all([nationality, gender]):
            return {'message': 'Missing Fields required'}, 400
        tourist = TouristInfoModel(nationality=nationality, gender=gender,
                                   user_id=user_id)
        try:
            tourist.save_to_db()
        except:
            return {'message': 'An error occured while creating tourists'}, 500
        return tourist.json(), 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(user_id)
        if tourist_user is None:
            return {'message': 'User must be a registered tourist'}
        nationality = request.json.get('nationality')
        gender = request.json.get('gender')
        tourist_user.nationality = nationality
        tourist_user.gender = gender
        try:
            tourist_user.save_to_db()
        except:
            return {'message': 'An error occured while editing tourists'}, 500
        return tourist_user.json()

class TouristDetail(Resource):
    @jwt_required()
    def post(self):
        current_identity = get_jwt_identity()
        detail_author = TouristInfoModel.find_by_user_id(current_identity)
        if detail_author is None:
            return {'message': 'User is not a registered tourist'}, 401
        tour_id = request.json.get('tour_id')
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        travel_buddies = request.json.get('travel_buddies')
        estimated_cost = request.json.get('estimated_cost')

        if not all([tour_id, departure, transportation, estimated_cost]):
            return {'message': 'Missing Fields required'}, 400
        if detail_author.user.email in travel_buddies:
            return {'message':
                    'You cannot add yourself into the travel buddy list'}, 400

        tour_instance = TourModel.find_by_id(tour_id)
        if tour_instance is None:
            return {'message': 'This tour does not exist'}, 400

        tourists = TouristInfoModel.query.join(UserModel).filter(
                                    UserModel.email.in_(travel_buddies)).filter(
                                    UserModel.isactive==True).all()
        if len(tourists) != len(travel_buddies):
            return {'message': 'All users must be registered tourists'}, 400

        detail = DetailModel(tour_id=tour_id, departure=departure,
                                transportation=transportation,
                                travel_buddies_created_by=detail_author.id,
                                estimated_cost=estimated_cost)
        tourists.append(detail_author)
        for tourist in tourists:
            tourist.tour_details_of_tourists.append(detail)
        try:
            tourist.save_to_db()
        except:
            return{'message':
                         'An error occured while trying to insert details'}, 500
        return tourist.with_details_json(), 201

    @jwt_required()
    def get(self):
        tourist_instances = TouristInfoModel.query.options(
                                                    joinedload('details_info'))
        tourists = [tourist.with_details_json() for tourist in tourist_instances]
        return tourists

    @jwt_required()
    def put(self):
        current_identity = get_jwt_identity()
        detail_author = TouristInfoModel.find_by_user_id(current_identity)
        if detail_author is None:
            return {'message': 'User is not a registered tourist'}, 401

        detail_id = request.json.get('detail_id')
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        travel_buddies = request.json.get('travel_buddies')
        estimated_cost = request.json.get('estimated_cost')

        detail_instance = DetailModel.find_by_id(detail_id)
        if (detail_instance is None or
                detail_author.id != detail_instance.travel_buddies_created_by):
            return {'message': 'Detail does not exist'}, 400

        if not all([detail_id, departure, transportation, estimated_cost]):
            return {'message': 'Missing Fields required'}, 400

        tourists = TouristInfoModel.query.join(UserModel).filter(
                                    UserModel.email.in_(travel_buddies)
                                    ).filter(UserModel.isactive==True).all()
        if len(tourists) != len(travel_buddies):
            return {'message':
                        'All travel buddies must be registered tourists'}, 400

        if detail_author.user.email in travel_buddies:
            return {'message':
                    'You cannot add yourself into the travel buddy list'}, 400
        tourists.append(detail_author)
        new_travel_buddies = list(set(tourists) - set(
                                        detail_instance.tourists_info.all()))
        to_be_replaced_travel_buddies = list(
                    set(detail_instance.tourists_info.all()) - (set(tourists)))

        detail_instance.id = detail_id
        detail_instance.departure = departure
        detail_instance.transportation = transportation
        detail_instance.estimated_cost = estimated_cost
        for tourist_info in detail_instance.tourists_info:
            if tourist_info in to_be_replaced_travel_buddies:
                detail_instance.tourists_info.remove(tourist_info)
        detail_instance.tourists_info.extend(new_travel_buddies)

        try:
            detail_instance.save_to_db()
        except:
            return{'message':
                        'An error occured while trying to update details'}, 500
        return detail_instance.with_tourist_json()


class AdminTouristList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(user_id)
        if tourist_user.role_id == 1 or tourist_user.role_id == 2:
            tourists = TouristInfoModel.query.join(UserModel,
                                                    TouristInfoModel.user).all()
            return {'tourists': [tourist.json_with_role()
                                        for tourist in tourists]}
        return {'message': 'Unauthorized User'}

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_user_id)
        if current_user is None:
            return {'message': 'User must be a registered tourist'}
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}
        user_id = request.json.get('user_id')
        user_instance = UserModel.query.get(user_id)

        nationality = request.json.get('nationality')
        gender = request.json.get('gender')
        role_id = request.json.get('role_id')
        if not all([user_id, nationality, gender, role_id]):
            return {'message': 'Missing Fields required'}, 400

        if user_instance is None:
            return {'message': 'user id does not exist'}, 400

        if TouristInfoModel.find_by_user_id(user_id):
            return {'message': 
                "A tourist with userid '{}' already exists".format(user_id)}, 400

        tourist = TouristInfoModel(nationality=nationality, gender=gender,
                                   user_id=user_id, role_id=role_id)
        try:
            tourist.save_to_db()
        except:
            return {'message': 'An error occured while creating tourists'}, 500
        return tourist.json_with_role(), 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user is None:
            return {'message': 'User must be a registered tourist'}
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}
        tourist_id = request.json.get('tourist_id')

        tourist_instance = TouristInfoModel.query.get(tourist_id)
        if tourist_instance is None:
            return {'message': 'tourist id does not exist'}, 400

        if current_user.role_id != 1 and tourist_instance.role_id == 1:
            return {'message': 'Only super admins are allowed'}, 400

        if tourist_instance.role_id == 2 and current_user.role_id ==2:
            return {'message': 'Admin cannot edit self or other Admins'}, 400
        nationality = request.json.get('nationality')
        gender = request.json.get('gender')
        role_id = request.json.get('role_id')
        if not all([tourist_id, nationality, gender, role_id]):
            return {'message': 'Missing Fields required'}

        tourist_instance.nationality = nationality
        tourist_instance.gender = gender
        tourist_instance.role_id = role_id

        try:
            tourist_instance.save_to_db()
        except:
            return {'message': 'An error occured while editing tourists'}, 500
        return tourist_instance.json_with_role()

class AdminForSpecificTourist(Resource):
    @jwt_required()
    def get(self, tourist_id):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user is None:
            return {'message': 'User must be a registered tourist'}
        tourist = TouristInfoModel.query.get(tourist_id)
        if tourist is None:
            return {'message': 'tourist does not exist'}, 404
        if current_user.role_id == 1 or current_user.role_id == 2:
            return tourist.json_with_role()
        return {'message': 'Unauthorized User'}
