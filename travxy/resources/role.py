from flask_restful import Resource, request
from travxy.models.role import RoleModel
from travxy.models.tourist import TouristInfoModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_identity


class RoleList(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        tourist_user = TouristInfoModel.find_by_user_id(current_identity)
        if (current_identity) and (tourist_user.role_id == 1 or tourist_user.role_id == 2):
            roles = [role.json() for role in RoleModel.find_all()]
            return {'roles': roles}
        return {'message': 'Unauthorized User'}