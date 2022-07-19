from flask_restful import Resource, request
from travxy.models.detail import DetailModel

from travxy.models.tourist import TouristInfoModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class DetailList(Resource):
    def get(self):
        details = [detail.json() for detail in DetailModel.find_all()]
        return {'details': details}

    @jwt_required()
    def post(self):
        tour_name = request.json.get('tour_name')
        departure = request.json.get('departure')
        transportation = request.json.get('transportation')
        experience = request.json.get('experience')
        upvote = request.json.get('upvote')
        estimated_cost = request.json.get('estimated_cost')
        category_id = request.json.get('category_id')
        user_tour_name = DetailModel.find_by_name(tour_name)

        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}
        tourist_details = tourist_user.tour_details_of_tourists.all()
        for tourist_detail in tourist_details:
            detail_id = user_tour_name.tour_name
            if detail_id == tourist_detail.tour_name:
                return {'message': "A tour with name '{}' already exists".format(tour_name)}, 400
        detail = DetailModel(tour_name, departure, transportation, experience, upvote,
                                estimated_cost, category_id)
        tourist_user.tour_details_of_tourists.append(detail)
        try:
            tourist_user.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert details'}, 500
        return tourist_user.json(), 201