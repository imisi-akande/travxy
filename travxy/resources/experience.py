from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from travxy.models.experience import TouristExperienceModel
from travxy.models.tourist import TouristInfoModel
from travxy.models.detail import DetailModel
from travxy.models.user import UserModel

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
        duration = request.json.get('duration')
        if not all([detail_id, comment, rating]):
            return {'message': 'Missing Required fields'}, 400
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
                                            comment=comment, rating=rating,
                                            duration=duration)
        try:
            experience.save_to_db()
        except:
            return{'message': 
                    'An error occured while trying to insert tourist experience'}, 500
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
        duration = request.json.get('duration')

        if not all([detail_id, comment, rating]):
            return {'message': 'Missing Required fields'}, 400
        detail_instance = DetailModel.query.join(TouristInfoModel,
                                    DetailModel.tourists_info).filter(
                                    DetailModel.id==detail_id,
                                    TouristInfoModel.id==tourist_id).all()
        if not detail_instance:
            return {'message': 'This detail does not exist'}, 404

        experience_instance = TouristExperienceModel.query.filter_by(
                                tourist_id=tourist_id,
                                detail_id=detail_id).first()
        if experience_instance is None:
            return {'message': 'Tourist experience id does not exist'}, 400
        experience_instance.detail_id = detail_id
        experience_instance.comment = comment
        experience_instance.rating = rating
        experience_instance.duration = duration

        try:
            experience_instance.save_to_db()
        except:
            return{'message': 
                    'An error occured while trying to insert tourist experience'}, 500
        return experience_instance.json(), 201

class TouristExperienceList(Resource):
    @jwt_required()
    def get(self):
        inactive_users = TouristInfoModel.query.join(UserModel).filter(
                                        UserModel.isactive==False).all()
        inactive_tourists_list = []
        for instance in inactive_users:
            inactive_tourists_list.append(instance.id)
        experience_instances = TouristExperienceModel.query.join(
                                TouristInfoModel.user).filter(
                                TouristExperienceModel.tourist_id.notin_(
                                inactive_tourists_list)).all()

        return {'tourists_experience':[experience_instance.json() 
                        for experience_instance in experience_instances]}, 200

class GetTouristExperience(Resource):
    @jwt_required()
    def get(self, tourist_id, detail_id):
        inactive_users = TouristInfoModel.query.join(UserModel).filter(
                                        UserModel.isactive==False).all()
        inactive_tourists_list = []
        for instance in inactive_users:
            inactive_tourists_list.append(instance.id)

        experience_instance = TouristExperienceModel.query.filter_by(
                            tourist_id=tourist_id).filter_by(
                            detail_id=detail_id).first()
        if experience_instance is None or tourist_id in inactive_tourists_list:
            return {'message': 'Experience does not exist'}, 400

        return experience_instance.json(), 200

    @jwt_required()
    def delete(self, tourist_id, detail_id):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message': 'User is not a registered tourist'}, 400
        experience_instance = TouristExperienceModel.query.filter_by(
                            tourist_id=tourist_id).filter_by(
                            detail_id=detail_id).first()
        if experience_instance is None or tourist_user.id != tourist_id:
            return {'message': 'Experience does not exist'}, 400
        try:
            experience_instance.delete_from_db()
        except:
            return{'message': 
            'An error occured while trying to delete tourist experience'}, 500
        return {'message': 'Experience deleted succesfully'}



