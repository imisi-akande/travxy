from flask_restful import Resource, request
from datetime import timedelta

from travxy.models.user import UserModel
from travxy.models.tourist import TouristInfoModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required, get_jwt)

from travxy.blocklist import BLOCKLIST

class UserRegister(Resource):
    def post(self):
        email = request.json.get('email')
        user = UserModel.find_by_email(email)
        if UserModel.find_by_email(email):
            return {"message":"User already exist"}, 400
        else:
            username = request.json.get('username')
            email = request.json.get('email')
            password = request.json.get('password')
            hash_password= UserModel.generate_hash(password)
            data = {'username':username, 'email':email,
                                'password':hash_password}
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "User created succesfully"}, 201

class AdminGetUser(Resource):
    @jwt_required()
    def get(self, user_id):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message':
                        'You must register as a tourist to see other tourists'}
        if (current_identity) and (tourist_user.role_id == 1
                                    or tourist_user.role_id == 2):
            user = UserModel.find_by_id(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            tourist_instance = TouristInfoModel.find_by_user_id(user_id)
            user_result = {'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'isactive': user.isactive,
                            'nationality': tourist_instance.nationality,
                            'gender': tourist_instance.gender }
            return user_result
        return {'message': 'Unauthorized User'}

    @jwt_required()
    def delete(self, user_id):
        user_instance = UserModel.query.get(user_id)
        if user_instance is None or user_instance.isactive==False:
            return {'message': 'User does not exist'}, 404
        current_identity = get_jwt_identity()
        current_user = TouristInfoModel.find_by_user_id(current_identity)

        if current_user is None:
            return {'message': 'User must be a registered tourist'}
        if current_user.role_id != 1 and current_user.role_id != 2:
            return {'message': 'Unauthorized User'}

        tourist_instance = TouristInfoModel.find_by_user_id(user_id)
        if current_user.role_id != 1 and tourist_instance.role_id == 1:
            return {'message': 'Only super admins are allowed'}, 400

        if current_user.role_id == 2 and tourist_instance.role_id ==2:
            return {'message': 'Admin cannot delete self or other Admins'}, 400

        user_instance.isactive = False
        user_instance.save_to_db()
        return {'message': 'User deleted succesfully'}, 200

class User(Resource):
    @jwt_required()
    def get(self, user_id):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message':
                        'You must register as a tourist to see other tourists'}
        user = UserModel.find_by_id(user_id)
        if not user or user.isactive==False:
            return {'message': 'User not found'}, 404
        return user.username_json()

    @jwt_required()
    def delete(self, user_id):
        current_identity = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user or user.isactive == False:
            return {'message': 'User not found'}, 404
        if user.id != current_identity:
            return {'message': 'Unauthorized User'}
        user.isactive = False
        user.save_to_db()
        return {'message': 'User deleted succesfully'}, 200

class UserLogin(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = UserModel.find_by_email(email)
        if not user:
            return {'message': 'Invalid Credentials'}, 401
        if user.isactive==False:
            return {'message': 'User account does not exist'}
        if user and user.check_hash(password):
            access_token = create_access_token(identity=user.id,
                                                fresh=timedelta(minutes=15))
            refresh_token = create_refresh_token(user.id)
            return {
                'message':'Login suceeded',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

class AdminGetUserList(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message':
                    'You must register as a tourist to view all other tourists'}
        if (current_identity) and (tourist_user.role_id == 1
                                    or tourist_user.role_id == 2):
            user_instance = UserModel.query.join(
                                TouristInfoModel, UserModel.tourist).filter(
                                UserModel.id==TouristInfoModel.user_id).all()
            users = {'users': [user.for_admin_with_tourist_json()
                                for user in user_instance]}
            return users
        return {'message': 'Unauthorized User'}, 401

class UserList(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if tourist_user is None:
            return {'message':
                    'You must register as a tourist to view all other tourists'}
        users = {'users': [user.username_json()
                            for user in UserModel.query.filter(
                                UserModel.isactive==True).all()]}
        return users

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200