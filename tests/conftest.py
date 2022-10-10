from re import T
import pytest
import os
from travxy import create_app
from travxy.db import db
from sqlalchemy.orm import close_all_sessions
from travxy.models.tourist import TouristInfoModel
from travxy.models.user import UserModel
from travxy.models.role import RoleModel
from travxy.models.detail import DetailModel
from travxy.models.place import PlaceModel


from flask_jwt_extended import create_access_token, create_refresh_token
from travxy.config import TestingConfig
import psycopg2


@pytest.fixture(scope="session")
def app():
    username = os.environ.get('TESTING_POSTGRES_USER')
    password = os.environ.get('TESTING_POSTGRES_PW')
    db_host = os.environ.get('TESTING_POSTGRES_HOST')
    db_name = os.environ.get('TESTING_POSTGRES_DB')
    conn = psycopg2.connect(dbname="postgres", user=username,
                                password=password, host=db_host)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.close()
    conn.close()
    app = create_app(TestingConfig)

    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()

@pytest.fixture(autouse=True)
def db_setup(app):
    db.create_all()
    yield db
    close_all_sessions()
    db.drop_all()

@pytest.fixture(autouse=True)
def create_roles(db_setup):
    roles = ["Super Admin", "Admin", "Regular"]
    role_instances = [RoleModel(id=i+1, name=role) for i, role in enumerate(roles)]
    db.session.bulk_save_objects(role_instances)
    db.session.commit()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_user():
    def _(user_details=None):
        if not user_details:
            user_details = {
                "last_name": "Stone",
                "first_name": "Mark",
                "username": "stone",
                "email": "stone@gmail.com",
                "password": "stone"
            }
        user_details["password"] = UserModel.generate_hash(user_details["password"])
        user = UserModel(**user_details)
        user.save_to_db()
        return user
    return _

@pytest.fixture
def create_jwt_token(create_user):
    def _(user=None):
        if not user:
            user = create_user()
        return user, create_access_token(identity=user.id, fresh=True)
    return _

@pytest.fixture
def create_refresh_jwt_token(create_user):
    def _(user=None):
        if not user:
            user = create_user()
        return user, create_refresh_token(identity=user.id)
    return _

@pytest.fixture
def create_tourist(create_user):
    def _(user=None, tourist_details=None):
        if not user:
            user = create_user()
        if not tourist_details:
            tourist_details = {
                "nationality": "Jamaica",
                "gender": "Male",
            }
        tourist_details['user_id'] = user.id
        tourist = TouristInfoModel(**tourist_details)
        tourist.save_to_db()
        return tourist
    return _

@pytest.fixture
def create_super_admin():
    def _(user_details=None):
        if not user_details:
            user_details = {
                "last_name": "Test",
                "first_name": "SuperAdmin",
                "username": "superadmin",
                "email": "superadmin@gmail.com",
                "role_id": 1,
                "password": "superadmin"
            }
        user_details["password"] = UserModel.generate_hash(user_details["password"])
        super_user = UserModel(**user_details)
        super_user.save_to_db()
        return super_user
    return _

@pytest.fixture
def create_super_user_jwt_token(create_super_admin):
    def _(super_user=None):
        if not super_user:
            super_user = create_super_admin()
        return super_user, create_access_token(identity=super_user.id, fresh=True)
    return _

@pytest.fixture
def create_admin():
    def _(user_details=None):
        if not user_details:
            user_details = {
                "last_name": "Test",
                "first_name": "Admin",
                "username": "admin",
                "email": "admin@gmail.com",
                "role_id": 2,
                "password": "admin"
            }
        user_details["password"] = UserModel.generate_hash(user_details["password"])
        user = UserModel(**user_details)
        user.save_to_db()
        return user
    return _

@pytest.fixture
def create_admin_jwt_token(create_admin):
    def _(admin_user=None):
        if not admin_user:
            admin_user = create_admin()
        return admin_user, create_access_token(identity=admin_user.id, fresh=True)
    return _

@pytest.fixture
def create_place():
    def _(place_details=None):
        if not place_details:
            place_details = {"name": "Hollywood",
                            "location": "Los Angeles",
                            "country": "United States of America",
                            "about": "Sight different people"}

        place = PlaceModel(**place_details)
        place.save_to_db()
        return place
    return _

@pytest.fixture
def create_detail(create_user, create_tourist, create_place):
    def _(user=None, place=None, place_details=None):
        if not user:
            users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
                }) for i in range(3)]
        for usr in users:
            create_tourist(user=usr)
        travel_buddies = ["test_user0@gmail.com", "test_user1@gmail.com", "test_user2@gmail.com"]
        tourists = TouristInfoModel.query.join(UserModel).filter(
                                    UserModel.email.in_(travel_buddies)).all()
        if not place:
            place = create_place()

        if not place_details:
            place_details = {"place_id": place.id,
                            "departure": "Austria",
                            "transportation": "Air",
                            "travel_buddies_created_by": 1,
                            "estimated_cost": 2500}
        detail = DetailModel(**place_details)
        for tourist in tourists:
            tourist.place_details_of_tourists.append(detail)
            tourist.save_to_db()
        return tourist
    return _