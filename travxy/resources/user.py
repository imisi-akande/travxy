from flask_restful import Resource, request
from datetime import timedelta

from travxy.models.user import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                get_jwt_identity, jwt_required)

class UserRegister(Resource):

    def post(self):
        email = request.json.get('email')
        if UserModel.find_by_email(email):
            return {"message":"User already exist"}, 400
        else:
            username = request.json.get('username')
            email = request.json.get('email')
            password = request.json.get('password')
            data = {'username':username, 'email':email, 'password':password}
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "User created succesfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted succesfully'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        email = request.json.get('email')
        password = request.json.get('password')
        user = UserModel.find_by_email(email)

        if user and user.check_hash(password):
            access_token = create_access_token(identity=user.id, fresh=timedelta(minutes=15))
            refresh_token = create_refresh_token(user.id)
            return {
                'message':'Login suceeded',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credentials'}, 401

class UserList(Resource):
    def get(self):
        categories = {'users': [user.json() for user in UserModel.query.all()]}
        return categories

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200