from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from hmac import compare_digest

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str, 
                        required=True, 
                        help="This Field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {"message":"User already exist"}, 400

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
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        type=str, 
                        required=True, 
                        help="This Field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credentials'}, 401

class UserList(Resource):
    def get(self):
        categories = {'users': [user.json() for user in UserModel.query.all()]}
        return categories