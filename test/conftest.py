import pytest
import os
from travxy import create_app, db
from flask_jwt_extended import create_access_token
from travxy.config import TestingConfig
import psycopg2


@pytest.fixture
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
    app = create_app(TestingConfig)

    ctx = app.app_context()
    ctx.push()
    db.create_all()

    yield app
    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_jwt_token():
    def _(user):
        create_access_token(identity=user.id, fresh=True)
    return _