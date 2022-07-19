from travxy.models.tourist import TouristInfoModel
from flask_restful import Resource, request

class TouristList(Resource):
    def get(self):
        tourists = [tourist.json() for tourist in TouristInfoModel.find_all()]
        return tourists

    def post(self):
        user_id = request.json.get('user_id')
        if TouristInfoModel.find_by_id(user_id):
            return {'message': "A tourist with userid '{}' already exists".format(user_id)}, 400

        nationality = request.json.get('nationality')
        gender = request.json.get('gender', 'Neutral')
        tourist = TouristInfoModel(nationality, gender, user_id)
        tourist_dict = tourist.json()
        try:
            tourist.save_to_db()
        except:
            return {'message': 'An error occured while creating tourists'}, 500
        return tourist_dict, 201