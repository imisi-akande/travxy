import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from travxy.models.tour import TourModel

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

    @jwt_required()
    def get(self, name):
        tour = TourModel.find_by_name(name)
        if tour:
            return tour.json()
        return {'message': 'Tour does not exist'}, 404

    @jwt_required()
    def post(self, name):
        if TourModel.find_by_name(name):
            return {"message": "An tour with the name {} already exists".format(name)}, 400

        data = Tour.parser.parse_args()
        tour = TourModel(name, data['location'], data['about'])
        try:
            tour.insert()
        except:
            return{'message': 'An error occured while trying to insert the tour'}, 500
        return tour.json(), 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()
        query = "DELETE FROM tours WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return{'message': 'Tour deleted succesfully'}, 200

    @jwt_required()
    def put(self, name):
        data = Tour.parser.parse_args()
        tour = TourModel.find_by_name(name)
        updated_tour = TourModel(name, data['location'], data['about'])
        if tour is None:
            try:
                updated_tour.insert()
            except:
                return{"message": "An error occured inserting the tour"}, 500
        else:
            try:
                updated_tour.update()
            except:
                return{"message": "An error occured updating the tour"}, 500
        return updated_tour.json()


class TourList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM tours" 
        result = cursor.execute(query)

        tours = []
        for row in result:
            tours.append({'name': row[0], 'location': row[1], 'about': row[2]})
            tours.append(row)

        connection.close()
        return {'tours': tours}
