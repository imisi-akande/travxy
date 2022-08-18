from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from travxy.models.category import CategoryModel
from travxy.models.tourist import TouristInfoModel

class Category(Resource):
    @jwt_required()
    def get(self, id):
        category = CategoryModel.find_by_id(id)
        if category:
            return category.with_tour_json()
        return {'message': 'Category not found'}, 404

class CategoryList(Resource):
    @jwt_required(optional=True)
    def get(self):
        current_identity = get_jwt_identity()
        categories = [category.with_tour_json() for category in CategoryModel.find_all()]
        if current_identity:
            return {'categories': categories}
        return {'categories': [category['name'] for category in categories],
                'message': 'More information available if you log in'}

class AdminCategoryList(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        name = request.json.get('name')
        if not name:
            return {'message': "Name required"}, 400
        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{}' already exists".format(name)}, 400

        category = CategoryModel(name=name)
        try:
            category.save_to_db()
        except:
            return {'message': 'An error occured while creating category'}, 500
        return category.json(), 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        id = request.json.get('id')
        name = request.json.get('name')
        category_instance = CategoryModel.query.get(id)
        category_instance.name = name
        try:
            category_instance.save_to_db()
        except:
            return {'message': 'An error occured while updating category'}, 500
        return category_instance.json(), 201

class AdminCategory(Resource):
    @jwt_required(fresh=True)
    def delete(self, id):
        user_id = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(user_id)
        if not current_user:
            return {'message': 'User must be a registered tourist'}
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}, 401
        category = CategoryModel.find_by_id(id)
        if category is None:
            return {'message': 'Category does not exist'}, 400
        try:
            category.delete_from_db()
        except:
            return {'message': 'An error occured while deleting category'}, 500
        return {'message': 'Category deleted'}
