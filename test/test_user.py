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

def test_logout(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/logout',  headers=headers)
    assert response.status_code==200
    assert response.json['message']

def test_get_users(client, create_jwt_token, create_user,
                    create_tourist):
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

def test_get_user(client, create_jwt_token, create_user,
                    create_tourist):
    user, access_token = create_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}

    create_tourist(user=user)
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(3)]
    test_user = users[1]
    response = client.get(f'/user/{test_user.id}', headers=headers)
    response_body = response.json
    assert response_body["username"]==test_user.username
    assert response.status_code==200

def test_get_user_account(client, create_jwt_token, create_tourist):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    response = client.get(f'/user/account/{user.id}', headers=headers)
    assert response.status_code==200

def test_edit_user(client, create_jwt_token):
    user, access_token = create_jwt_token()
    user_details = {
                    "last_name": "Stone",
                    "first_name": "Miriam" }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.put(f'/user/{user.id}', headers=headers, json=user_details)
    assert response.json['message']
    assert response.status_code==200

def test_delete_user(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.delete(f'/user/{user.id}', headers=headers)
    assert response.json['message']
    assert response.status_code==200

def test_super_admin_get_users_list(client, create_super_user_jwt_token, create_user):
    user, access_token = create_super_user_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(5)]
    response = client.get('/admin/users', headers=headers)
    response_body = response.json
    assert len(response.json['users']) == 6
    assert response.status_code==200

def test_admin_get_users_list(client, create_admin_jwt_token, create_user):
    user, access_token = create_admin_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(5)]
    response = client.get('/admin/users', headers=headers)
    response_body = response.json
    assert len(response.json['users']) == 6
    assert response.status_code==200

def test_admin_add_user(client, create_super_user_jwt_token):
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    user_detail = {"last_name": "Test",
                "first_name": "User",
                "username": "new_user",
                "email": "new_user@gmail.com",
                "password": "password"}
    response = client.post('/admin/user', headers=headers, json=user_detail)
    assert response.status_code==201
    assert response.json['message']

def test_super_admin_edit_user(client, create_super_user_jwt_token, create_user):
    user, access_token = create_super_user_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}
    user_detail = {"last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password"}
    test_user = create_user(user_detail)
    new_user_detail = {
        "last_name": "Test5",
        "first_name": "User5",
        "role_id": 2
    }
    response = client.put(f'/admin/user/{test_user.id}', headers=headers, json=new_user_detail)
    assert response.status_code==200
    assert response.json['message']

def test_super_admin_delete_user(client, create_super_user_jwt_token, create_user):
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(2)]
    test_user = users[1]
    response = client.delete(f'/admin/user/{test_user.id}', headers=headers)
    assert response.json['message']
    assert response.status_code==200

def test_admin_delete_user(client, create_admin_jwt_token, create_user):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(2)]
    test_user = users[1]
    response = client.delete(f'/admin/user/{test_user.id}', headers=headers)
    assert response.json['message']
    assert response.status_code==200

def test_token_refresh(client, create_refresh_jwt_token):
    user, refresh_token = create_refresh_jwt_token()
    headers = {"Authorization":f"Bearer {refresh_token}"}
    response = client.post('/refresh', headers=headers)
    assert response.status_code==200
