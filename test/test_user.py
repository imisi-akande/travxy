def test_register(client):
    user_details = {
        "last_name": "Stone",
        "first_name": "Miriam",
        "username": "stone",
        "email": "stone@gmail.com",
        "password": "stone"
    }
    response = client.post('/register', json=user_details)
    assert response.status_code==201
    assert response.json['message']

def test_login(client, create_user):
    create_user()
    user_details = {
        "email": "stone@gmail.com",
        "password": "stone"
    }
    response = client.post('/login', json=user_details)
    assert response.status_code==200
    assert response.json['message']

