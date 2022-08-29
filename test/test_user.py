import pytest

from test.conftest import app
from travxy import create_app, db
import travxy.models.user as user

def test_register(client):
    user_details = {
        "username": "stone",
        "email": "stone@gmail.com",
        "password": "stone"
    }
    response = client.post('/register', json=user_details)
    assert response.status_code==201
    assert response.json['message']