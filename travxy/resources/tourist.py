from travxy.models.tourist import TouristInfoModel
from travxy.models.tour import TourModel
from travxy.models.detail import DetailModel
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload


class TouristList(Resource):
    @jwt_required()
    def get(self):
        tourist_instances = TouristInfoModel.query.options(joinedload('details_info'))
        tourists = [tourist.with_details_json() for tourist in tourist_instances]
        return tourists

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if TouristInfoModel.find_by_id(user_id):
            return {'message': "A tourist with userid '{}' already exists".format(user_id)}, 400

        nationality = request.json.get('nationality')
        gender = request.json.get('gender', 'Neutral')
        tourist = TouristInfoModel(nationality, gender, user_id)
        try:
            tourist.save_to_db()
        except:
            return {'message': 'An error occured while creating tourists'}, 500
        return tourist.json(), 201

class TouristDetail(Resource):
    @jwt_required()
    def post(self):
        tour_name = request.json.get('tour_name')
        #tour_id = DetailModel.find_by_id(tour_id)
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        experience = request.json.get('experience')
        upvote = request.json.get('upvote')
        estimated_cost = request.json.get('estimated_cost')
        tour_instance = TourModel.find_by_name(tour_name)
        tour_id = tour_instance.id

        if tour_instance is None:
            return {'message': 'This tour name does not exist'}, 400
        category_id = tour_instance.category_id
        detail_instance = DetailModel.find_by_id(tour_id)
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}
        tourist_details = tourist_user.tour_details_of_tourists.all()
        for tourist_detail in tourist_details:
            if detail_instance is not None:
                detail_id = detail_instance.tour_id
                if detail_id == tourist_detail.tour_id:
                    return {'message': "A tour with name '{}' already exists".format(tour_name)}, 400
        detail = DetailModel(tour_id, tour_name, departure, transportation, experience, upvote,
                                estimated_cost, category_id)
        tourist_user.tour_details_of_tourists.append(detail)
        try:
            tourist_user.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert details'}, 500
        return detail.json(), 201