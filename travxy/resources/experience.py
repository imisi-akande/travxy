from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from travxy.models.experience import TouristExperienceModel
from travxy.models.tourist import TouristInfoModel
from travxy.models.detail import DetailModel

class TouristExperience(Resource):
    @jwt_required()
    def post(self):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}
        tourist_id = tourist_user.id
        detail_id = request.json.get('detail_id')
        comment = request.json.get('comment')
        rating = request.json.get('rating')
        detail_instance = DetailModel.query.join(TouristInfoModel,
                                    DetailModel.tourists_info).filter(
                                    DetailModel.id==detail_id,
                                    TouristInfoModel.id==tourist_id).all()
        if not detail_instance:
            return {'message': 'This detail does not exist'}, 404

        if TouristExperienceModel.query.filter_by(tourist_id=tourist_id,
                                                detail_id=detail_id).first():
            return {'message': 'Tourist Experience already exists for this trip'}
        experience = TouristExperienceModel(tourist_id=tourist_id,
                                            detail_id=detail_id,
                                            comment=comment, rating=rating)
        try:
            experience.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert tourist experience'}
        return experience.json(), 201

    @jwt_required()
    def put(self):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}
        tourist_id = tourist_user.id
        detail_id = request.json.get('detail_id')
        comment = request.json.get('comment')
        rating = request.json.get('rating')
        detail_instance = DetailModel.query.join(TouristInfoModel,
                                    DetailModel.tourists_info).filter(
                                    DetailModel.id==detail_id,
                                    TouristInfoModel.id==tourist_id).all()
        if not detail_instance:
            return {'message': 'This detail does not exist'}, 404

        experience_instance = TouristExperienceModel.query.filter_by(
                                tourist_id=tourist_id,
                                detail_id=detail_id).first()
        experience_instance.detail_id = detail_id
        experience_instance.comment = comment
        experience_instance.rating = rating
        try:
            experience_instance.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert tourist experience'}
        return experience_instance.json(), 201

class TouristExperienceList(Resource):
    @jwt_required()
    def get(self):
        return {'tourists_experience':[experience.json() for experience in
                                        TouristExperienceModel.find_all()]}

