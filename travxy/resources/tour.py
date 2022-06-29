from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.tour import TourModel

class Tour(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str, 
                        required=True, 
                        help="This Field cannot be blank")

    parser.add_argument('location',
                        type=str, 
                        required=True, 
                        help="This Field cannot be blank")

    parser.add_argument('about',
                        type=str, 
                        required=True, 
                        help="This Field cannot be blank")
    parser.add_argument('category_id',
                        type=int, 
                        required=True, 
                        help="Every tour needs a category id")


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
        data = Tour.parser.parse_args()
        tour = TourModel.find_by_name(name)
        if tour is None:
            tour = TourModel(name, **data)
        else:
           tour.name = data['name']
           tour.location = data['location']
           tour.about = data['about']
        tour.save_to_db()
        return tour.json()


class TourList(Resource):
    @jwt_required()
    def get(self):
        return {'tours':[tour.json() for tour in TourModel.query.all()]}

    @jwt_required()
    def post(self):
        data = Tour.parser.parse_args()
        name = data.get('name')
        if TourModel.find_by_name(name):
            return {"message": "An tour with the name {} already exists".format(name)}, 400

        tour = TourModel(**data)
        try:
            tour.save_to_db()
        except:
            return{'message': 'An error occured while trying to insert the tour'}, 500
        return tour.json(), 201

