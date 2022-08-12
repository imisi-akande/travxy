from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from travxy.models.tour import TourModel

class Tour(Resource):

    @jwt_required()
    def get(self, tour_id):
        tour = TourModel.find_by_id(tour_id)
        if tour:
            return tour.json()
        return {'message': 'Tour does not exist'}, 404

    @jwt_required()
    def delete(self, tour_id):
        tour = TourModel.find_by_id(tour_id)
        if tour:
            tour.delete_from_db()
            return{'message': 'Tour deleted succesfully'}, 200
        return {'message': 'Tour does not exist'}

class TourList(Resource):
    @jwt_required()
    def get(self):
        return {'tours':[tour.json() for tour in TourModel.find_all()]}

    @jwt_required()
    def post(self):
        name = request.json.get('tour_name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')
        category_id = request.json.get('category_id')
        tour = TourModel(name=name, location=location, country=country,
                            about=about, category_id=category_id)
        try:
            tour.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert the tour'}, 500
        return tour.json(), 201

    @jwt_required()
    def put(self):
        tour_id = request.json.get('tour_id')
        name = request.json.get('name')
        location = request.json.get('location')
        country = request.json.get('country')
        about = request.json.get('about')
        category_id = request.json.get('category_id')

        tour = TourModel.find_by_id(tour_id)
        if tour is None:
            return {'message': 'Tour does not exist'}
        else:
           tour.tour_id = tour_id
           tour.name = name
           tour.location = location
           tour.country = country
           tour.about = about
           tour.category_id = category_id
           tour.save_to_db()
        return tour.json()




