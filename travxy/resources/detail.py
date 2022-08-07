from flask_restful import Resource, request
from travxy.models.detail import DetailModel
from travxy.models.tourist import TouristInfoModel
from travxy.models.tour import TourModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload


class DetailList(Resource):
    @jwt_required()
    def get(self):
        detail_instances = DetailModel.query.options(joinedload('tourists'))
        details = [detail.with_tourist_json() for detail in detail_instances]
        return details

    @jwt_required()
    def post(self):
        tour_name = request.json.get('tour_name')
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        experience = request.json.get('experience')
        upvote = request.json.get('upvote')
        estimated_cost = request.json.get('estimated_cost')
        tour_instance = TourModel.find_by_name(tour_name)
        if tour_instance is None:
            return {'message': 'This tour name does not exist'}, 400
        category_id = tour_instance.category_id
        detail_instance = DetailModel.find_by_name(tour_name)
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}
        tourist_details = tourist_user.tour_details_of_tourists.all()
        for tourist_detail in tourist_details:
            if detail_instance is not None:
                detail_name = detail_instance.tour_name
                if detail_name == tourist_detail.tour_name:
                    return {'message': "A tour with name '{}' already exists".format(tour_name)}, 400
        detail = DetailModel(tour_name, departure, transportation, experience, upvote,
                                estimated_cost, category_id)
        detail.tourists_info.append(tourist_user)
        try:
            detail.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert details'}, 500
        return detail.json(), 201