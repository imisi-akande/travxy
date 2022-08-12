from flask_restful import Resource, request
from travxy.models.detail import DetailModel
from travxy.models.user import UserModel
from travxy.models.tourist import TouristInfoModel
from travxy.models.tour import TourModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

class Detail(Resource):

    @jwt_required()
    def post(self):
        tour_id = request.json.get('tour_id')
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        travel_buddies = request.json.get('travel_buddies')
        estimated_cost = request.json.get('estimated_cost')

        if not all([tour_id, departure, transportation, estimated_cost]):
            return {'message': 'Missing Fields required'}, 400
        tour_instance = TourModel.find_by_id(tour_id)
        if tour_instance is None:
            return {'message': 'This tour does not exist'}, 400

        tourists = TouristInfoModel.query.join(UserModel).filter(UserModel.email.in_(travel_buddies)).all()
        if len(tourists) != len(travel_buddies):
            return {'message': 'All users must be registered tourists'}, 400

        current_identity = get_jwt_identity()
        detail_author = TouristInfoModel.find_by_user_id(current_identity)
        if detail_author is None:
            return {'message': 'User is not a registered tourist'}, 401

        if detail_author.user.email in travel_buddies:
            return {'message': 'You cannot add yourself into the travel buddy list'}, 400

        detail = DetailModel(tour_id=tour_id, departure=departure, transportation=transportation,
                            travel_buddies_created_by=detail_author.id, estimated_cost=estimated_cost)

        for tourist in tourists:
            detail.tourists_info.append(tourist)
        detail.tourists_info.append(detail_author)

        try:
            detail.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert details'}, 500
        return detail.json(), 201

    @jwt_required()
    def put(self):
        detail_id = request.json.get('detail_id')
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        travel_buddies = request.json.get('travel_buddies')
        estimated_cost = request.json.get('estimated_cost')

        if not all([detail_id, departure, transportation, estimated_cost]):
            return {'message': 'Missing Fields required'}, 400

        current_identity = get_jwt_identity()
        detail_author = TouristInfoModel.find_by_user_id(current_identity)

        detail_instance = DetailModel.find_by_id(detail_id)

        if detail_instance is None:
            return {'message': 'Detail does not exist'}

        tourists = TouristInfoModel.query.join(UserModel).filter(
                                    UserModel.email.in_(travel_buddies)).all()
        if len(tourists) != len(travel_buddies):
            return {'message': 'All travel buddies must be registered tourists'}, 400

        if detail_author.id != detail_instance.travel_buddies_created_by:
            return {'message': 'Detail does not exist'}, 404

        if detail_author.user.email in travel_buddies:
            return {'message': 'You cannot add yourself into the travel buddy list'}, 400
        tourists.append(detail_author)
        new_travel_buddies = list(set(tourists) - set(detail_instance.tourists_info.all()))
        to_be_replaced_travel_buddies = list(set(detail_instance.tourists_info.all()) - (set(tourists)))

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
            return{'message': 'An error occured while trying to update details'}, 500
        return detail_instance.with_tourist_json()

class DetailList(Resource):

    @jwt_required()
    def get(self):
        detail_instances = DetailModel.query.options(joinedload('tourists'))
        details = [detail.with_tourist_json() for detail in detail_instances]
        return details




