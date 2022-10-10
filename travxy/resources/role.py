from flask_restful import Resource, request
from travxy.models.role import RoleModel
from travxy.models.user import UserModel
from flask_jwt_extended import get_jwt_identity, jwt_required


class RoleList(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        current_user = UserModel.query.get(current_identity)
        role_instance = RoleModel.query.join(UserModel,
                                    RoleModel.users).all()
        if ((current_identity) and
                (current_user.role_id == 1 or current_user.role_id == 2)):
            roles = [role.json() for role in role_instance]
            return roles, 200
        return {'message': 'Unauthorized User'}, 401
