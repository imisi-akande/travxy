import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        tour = self.find_by_name(name)
        if tour:
            return tour
        return {'message': 'Tour does not exist'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tours WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'tour': {'name' : row[0], 'location': row[1], 
                    'about': row[2]}
               }

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An tour with the name {} already exists".format(name)}, 400

        data = Tour.parser.parse_args()
        tour = {'name': name, 'location':data['location'],
                'about': data['about']}
        try:
            self.insert(tour)
        except:
            return{'message': 'An error occured while trying to insert the tour'}, 500
        return tour, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()
        query = "DELETE FROM tours WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return{'message': 'Tour deleted succesfully'}, 200

    @classmethod
    def insert(cls, tour):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()

        query = "INSERT INTO tours VALUES (?, ?, ?)"
        cursor.execute(query, (tour['name'], tour['location'], tour['about']))
        connection.commit()
        connection.close()

    @jwt_required()
    def put(self, name):
        data = Tour.parser.parse_args()
        tour = self.find_by_name(name)
        updated_tour = {'name': name, 'location':data['location'],
                'about': data['about']}
        if tour is None:
            try:
                Tour.insert(updated_tour)
            except:
                return{"message": "An error occured inserting the tour"}, 500
        else:
            try:
                Tour.update(updated_tour)
            except:
                return{"message": "An error occured updating the tour"}, 500
        return updated_tour

    @classmethod
    def update(cls, tour):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()
        query = "UPDATE tours SET location=?, about=? WHERE name=?"
        cursor.execute(query, (tour['location'], tour['about'], tour['name']))
        connection.commit()
        connection.close()

class TourList(Resource):
   # @jwt_required()
    def get(self):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM tours"
        result = cursor.execute(query)

        tours = []
        for row in result:
            tours.append({'name': row[0], 'location': row[1], 'about': row[2]})

        connection.close()
        return {'tours': tours}
