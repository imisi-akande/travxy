from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from travxy.models.category import CategoryModel

class Category(Resource):
    @jwt_required()
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404


    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()
        return {'message': 'Category deleted'}

class CategoryList(Resource):
    @jwt_required()
    def get(self):
        categories = {'categories': [category.json() for category in CategoryModel.query.all()]}
        return categories

    @jwt_required()
    def post(self):
        name = request.json.get('name')
        if not name:
            return {'message': "Name required"}, 400
        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{}' already exists".format(name)}, 400

        category = CategoryModel(name)
        try:
            category.save_to_db()
        except:
            return {'message': 'An error occured while creating category'}, 500
        return category.json(), 201