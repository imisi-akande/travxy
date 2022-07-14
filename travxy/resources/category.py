from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_identity
from flask_restful import Resource, request
from travxy.models.category import CategoryModel

class Category(Resource):
    @jwt_required()
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404

    @jwt_required(fresh=True)
    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()
        return {'message': 'Category deleted'}

class CategoryList(Resource):
    @jwt_required(optional=True)
    def get(self):
        current_identity = get_jwt_identity()
        categories = [category.json() for category in CategoryModel.find_all()]
        if current_identity:
            return {'categories': categories}
        return {'categories': [category['name'] for category in categories],
                'message': 'More information available if you log in'
        }

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