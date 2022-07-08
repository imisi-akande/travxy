from travxy.models.tourist import TouristInfoModel, GenderChoices
from flask_restful import Resource, request
from flask import jsonify
import json

class TouristList(Resource):
    def get(self):
        tourists = [tourist.get_from_db() for tourist in TouristInfoModel.find_all()]
        return jsonify(tourists)

    def post(self):
        user_id = request.json.get('user_id')
        if TouristInfoModel.find_by_id(user_id):
            return {'message': "A tourist with userid '{}' already exists".format(user_id)}, 400

        nationality = request.json.get('nationality')
        gender = request.json.get('gender', 'Neutral')
        tourist = TouristInfoModel(nationality, gender, user_id)
        tour_dict = tourist.to_json()
        try:
            tourist.save_to_db()
        except:
            return {'message': 'An error occured while creating tourists'}, 500
        return jsonify(tour_dict)