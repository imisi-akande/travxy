from flask_restful import Resource, request
from travxy.models.detail import DetailModel
from travxy.models.user import UserModel
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
        travel_buddy_one = request.json.get('travel_buddy_one')
        travel_buddy_two = request.json.get('travel_buddy_two')
        travel_buddy_three = request.json.get('travel_buddy_three')

        experience = request.json.get('experience')
        upvote = request.json.get('upvote')
        estimated_cost = request.json.get('estimated_cost')
        tour_instance = TourModel.find_by_name(tour_name)
        tour_id = tour_instance.id

        if tour_instance is None:
            return {'message': 'This tour name does not exist'}, 400
        category_id = tour_instance.category_id
        user_instance= [user.json() for user in UserModel.query.all()]
        email_list = []
        for instance in user_instance:
            email_list.append(instance['email'])
        if (travel_buddy_one and travel_buddy_one not in email_list) or \
            (travel_buddy_two and travel_buddy_two not in email_list) or \
                (travel_buddy_three and travel_buddy_three not in email_list):
            return {'message': 'Travel buddy is not a registered tourist'}

        user_list = UserModel.query.options(joinedload('tourist'))
        users = [user.with_tourist_json() for user in user_list]
        for user in users:
            if travel_buddy_one == user['email']:
                travel_buddy_one = user['tourist_id']

            if travel_buddy_two == user['email']:
                travel_buddy_two = user['tourist_id']

            if travel_buddy_three == user['email']:
                travel_buddy_three = user['tourist_id']

        detail_instance = DetailModel.find_by_id(tour_id)
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}
        tourist_details = tourist_user.tour_details_of_tourists.all()
        for tourist_detail in tourist_details:
            if detail_instance is not None:
                detail_name = detail_instance.tour_id
                if detail_name == tourist_detail.tour_id:
                    return {'message': "A tour with name '{}' already exists".format(tour_name)}, 400
        detail = DetailModel(tour_id, tour_name, departure, transportation, travel_buddy_one, travel_buddy_two, travel_buddy_three, experience, upvote,
                                estimated_cost, category_id)
        travel_buddies = TouristInfoModel.query.filter(TouristInfoModel.id.in_((travel_buddy_one, travel_buddy_two, travel_buddy_three))).all()

        detail.tourists_info.append(tourist_user)
        for buddy in travel_buddies:
            detail.tourists_info.append(buddy)

        try:
            detail.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert details'}, 500
        return detail.json(), 201
