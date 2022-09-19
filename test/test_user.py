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

def test_get_users(client, create_jwt_token, create_user,
                        create_super_admin, create_tourist):
    user, access_token = create_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}

    create_tourist(user=user)
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(2)]
    for usr in users:
        create_tourist(user=usr)
    response = client.get('/users', headers=headers)
    response_body = response.json
    assert len(response_body['users']) == 3
    assert response_body['users'][0]["username"]==user.username
    assert response.status_code==200

def test_get_user(client, create_jwt_token, create_admin_user,
                        create_super_admin, create_tourist):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    response = client.get(f'/user/{user.id}', headers=headers)
    assert response.status_code==200

def test_admin_get_user(client, create_super_user_jwt_token, create_admin_user,
                        create_user, add_super_admin_to_tourist):
    user, access_token = create_super_user_jwt_token()
    create_user(),
    create_admin_user()
    headers = {"Authorization":f"Bearer {access_token}"}
    add_super_admin_to_tourist()
    response = client.get('/admin/user/3', headers=headers)
    print(user, 'the existence')
    print(response.json, 'poland')
    assert response.status_code==200
