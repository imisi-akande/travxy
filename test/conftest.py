import pytest
import os
from travxy import create_app, db
from sqlalchemy.orm import close_all_sessions
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
                "first_name": "Miriam",
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

