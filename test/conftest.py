from re import T
import pytest
import os
from travxy import create_app, db
from sqlalchemy.orm import close_all_sessions
from travxy.models.tourist import TouristInfoModel
from travxy.models.user import UserModel
from travxy.models.role import RoleModel

from flask_jwt_extended import create_access_token
from travxy.config import TestingConfig
import psycopg2


@pytest.fixture(scope="session")
def app():
    username = os.environ.get('TESTING_POSTGRES_USER')
    password = os.environ.get('TESTING_POSTGRES_PW')
    db_host = os.environ.get('TESTING_POSTGRES_HOST')
    conn = psycopg2.connect(dbname='postgres', user=username,
                                password=password, host=db_host)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS trav_api_test")
    cursor.execute("CREATE DATABASE trav_api_test")
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
                "id": 2,
                "last_name": "Kit",
                "first_name": "Paul",
                "username": "kit",
                "email": "kit@gmail.com",
                "password": "kit"
            }
        user_details["password"] = UserModel.generate_hash(user_details["password"])
        super_user = UserModel(**user_details)
        print(super_user.id, 'the adminnnn')
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
def add_super_admin_to_tourist():
    def _(tourist_details=None):
        if not tourist_details:
            # create_super_admin()
            tourist_details = {
                "id": 2,
                "nationality": "Ethiopia",
                "gender": "Male",
                "role_id": 1,
                "user_id": 2
            }
        tourist = TouristInfoModel(**tourist_details)
        tourist.save_to_db()
        return tourist
    return _

@pytest.fixture
def create_admin_user():
    def _(user_details=None):
        if not user_details:
            user_details = {
                "id": 3,
                "last_name": "Tyler",
                "first_name": "Sarah",
                "username": "tyler",
                "email": "tyler@gmail.com",
                "password": "tyler"
            }
        user_details["password"] = UserModel.generate_hash(user_details["password"])
        user = UserModel(**user_details)
        user.save_to_db()
        return user
    return _

@pytest.fixture
def create_admin_user_jwt_token(create_admin_user):
    def _(admin_user=None):
        if not admin_user:
            admin_user = create_admin_user()
        return admin_user, create_access_token(identity=admin_user.id, fresh=True)
    return _

@pytest.fixture
def add_admin_to_tourist():
    def _(tourist_details=None):
        if not tourist_details:
            # create_admin()
            tourist_details = {
                "id": 3,
                "nationality": "Zambia",
                "gender": "Female",
                "user_id": 3,
                "role_id": 2
            }
        tourist = TouristInfoModel(**tourist_details)
        tourist.save_to_db()
        return tourist
    return _

