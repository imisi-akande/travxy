from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from travxy.models.tourist import TouristInfoModel

from travxy.models.remarks import ApplicationExperienceModel

class Remarks(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)
        if current_user is None:
            return {'message': 'User is not a registered tourist'}, 401
        app_experience = [experience.json() for experience in ApplicationExperienceModel.query.all()]
        return {'experience': app_experience}, 200

    @jwt_required()
    def post(self):
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)
        if current_user is None:
            return {'message': 'User is not a registered tourist'}, 401
        comment = request.json.get("comment")
        rating = request.json.get('rating')
        if not all([comment, rating]):
            return {'message': 'Missing fields required'}, 400
        app_experience_instance = ApplicationExperienceModel(
                                            tourist_id=current_user.id,
                                            comment=comment, rating=rating)
        try:
            app_experience_instance.save_to_db()
        except:
            return{'message':
                    'An error occured while trying to insert remark'}, 500

        return app_experience_instance.json(), 201

class SpecificRemarks(Resource):
    @jwt_required()
    def get(self, tourist_id):
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)
        if current_user is None:
            return {'message': 'User is not a registered tourist'}, 401
        app_experience_instance = [experience.json()
                                    for experience in ApplicationExperienceModel.query.filter_by(
                                    tourist_id=tourist_id).all()]
        return {'experience': app_experience_instance}, 200


class EditRemarks(Resource):
    @jwt_required()
    def put(self, id):
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)
        if current_user is None:
            return {'message': 'User is not a registered tourist'}, 401

        comment = request.json.get("comment")
        rating = request.json.get('rating')
        if not all([comment, rating]):
            return {'message': 'Missing fields required'}, 400

        app_experience_instance = ApplicationExperienceModel.query.get(id)

        if current_user.id != app_experience_instance.tourist_id:
            return {'message': 'Unauthorized User'}, 400
        app_experience_instance.comment = comment
        app_experience_instance.rating = rating
        try:
            app_experience_instance.save_to_db()
        except:
            return{'message':
                    'An error occured while trying to insert remark'}, 500

        return app_experience_instance.json(), 201

    @jwt_required()
    def delete(self, id):
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)
        if current_user is None:
            return {'message': 'User is not a registered tourist'}, 401

        app_experience_instance = ApplicationExperienceModel.query.get(id)
        if app_experience_instance:
            if current_user.id != app_experience_instance.tourist_id:
                return {'message': 'Unauthorized User'}, 400
            app_experience_instance.delete_from_db()
            return{'message': 'Application experience deleted succesfully'}, 200
        return {'message': 'Application experience does not exist'}, 404