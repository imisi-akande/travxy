from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from travxy.models.tour import TourModel

class Tour(Resource):

    @jwt_required()
    def get(self, name):
        tour = TourModel.find_by_name(name)
        if tour:
            return tour.json()
        return {'message': 'Tour does not exist'}, 404

    @jwt_required()
    def delete(self, name):
        tour = TourModel.find_by_name(name)
        if tour:
            tour.delete_from_db()
        return{'message': 'Tour deleted succesfully'}, 200

    @jwt_required()
    def put(self, name):
        location = request.json.get('location')
        about = request.json.get('about')
        category_id = request.json.get('category_id')

        tour = TourModel.find_by_name(name)

        if tour is None:
            tour = TourModel(name, location, about, category_id)
        else:
           tour.name = name
           tour.location = location
           tour.about = about
           tour.category_id = category_id
           tour.save_to_db()
        return tour.json()


class TourList(Resource):
    @jwt_required()
    def get(self):
        return {'tours':[tour.json() for tour in TourModel.query.all()]}

    @jwt_required()
    def post(self):
        name = request.json.get('name')
        if TourModel.find_by_name(name):
            return {"message": "An tour with the name {} already exists".format(name)}, 400

        location = request.json.get('location')
        about = request.json.get('about')
        category_id = request.json.get('category_id')
        tour = TourModel(name, location, about, category_id)
        try:
            tour.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert the tour'}, 500
        return tour.json(), 201

