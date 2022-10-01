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

def test_register_user_already_exist(client, create_user):
    create_user()
    user_details = {
                "last_name": "Stone",
                "first_name": "Mark",
                "username": "stone",
                "email": "stone@gmail.com",
                "password": "stone"
            }
    response = client.post('/register', json=user_details)

    assert response.status_code==400
    assert response.json['message'] == "User already exist"

def test_register_username_already_exist(client, create_user):
    create_user()
    user_details = {
                "last_name": "Stone",
                "first_name": "Mark",
                "username": "stone",
                "email": "stone2000@gmail.com",
                "password": "stone"
            }
    response = client.post('/register', json=user_details)
    assert response.status_code==400
    assert response.json['message'] == "Username already exist"


def test_login(client, create_user):
    create_user()
    user_details = {
        "email": "stone@gmail.com",
        "password": "stone"
    }
    response = client.post('/login', json=user_details)
    assert response.status_code==200
    assert response.json['message']

def test_invalid_login(client, create_user):
    create_user()
    user_details = {
        "email": "hacker@gmail.com",
        "password": "stone"
    }
    response = client.post('/login', json=user_details)
    assert response.status_code==401
    assert response.json['message'] == "Invalid Credentials"

def test_inactive_user_login(client, create_user):
    create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password",
                "isactive": False
                })
    user_details = {
        "email": "test_user@gmail.com",
        "password": "password"
    }
    response = client.post('/login', json=user_details)
    assert response.status_code==400
    assert response.json['message'] == "User account does not exist"


def test_logout(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/logout',  headers=headers)
    assert response.status_code==200
    assert response.json['message']

def test_get_user_list(client, create_jwt_token, create_user,
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

def test_non_tourist_get_user_list(client, create_jwt_token, create_user,
                    create_tourist):
    user, access_token = create_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}

    # create_tourist(user=user)
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
    assert response.status_code==400
    assert response.json['message']=="You must register as a tourist to view all other tourists"

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

def test_non_tourist_get_user(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}

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
    assert response.status_code==401
    assert response_body['message'] == "You must register as a tourist to see other tourists"

def test_get_user_for_inactive_user(client, create_jwt_token, create_user,
                    create_tourist):
    user, access_token = create_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password",
                "isactive": False
            })
    response = client.get(f'/user/{regular_user.id}', headers=headers)
    response_body = response.json
    assert response.status_code==404
    assert response_body['message'] == "User not found"


def test_get_user_account(client, create_jwt_token, create_tourist):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    response = client.get(f'/user/account/{user.id}', headers=headers)
    assert response.status_code==200

def test_get_user_account_for_unauthorized_user(client, create_jwt_token,
                                                create_user, create_tourist):
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password",
                "isactive": False
            })
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    response = client.get(f'/user/account/{regular_user.id}', headers=headers)
    assert response.status_code==401
    assert response.json['message'] == "Unauthorized user"

def test_get_user_account_for_non_tourist_user(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.get(f'/user/account/{user.id}', headers=headers)
    assert response.status_code==401
    assert response.json['message'] == "Register as a tourist to see account profile"

def test_get_user_account_for_user_not_found(client, create_jwt_token,
                                                create_user, create_tourist):
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password",
                "isactive": False
            })
    user, access_token = create_jwt_token(regular_user)
    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    response = client.get(f'/user/account/{regular_user.id}', headers=headers)
    assert response.status_code==404
    assert response.json['message'] == "User not found"

def test_edit_user(client, create_jwt_token):
    user, access_token = create_jwt_token()
    user_details = {
                    "last_name": "Stone",
                    "first_name": "Miriam" }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.put(f'/user/{user.id}', headers=headers, json=user_details)
    assert response.json['message']
    assert response.status_code==200

def test_unauthorized_user_edit_user(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password"
            })
    user_details = {
                    "last_name": "Stone",
                    "first_name": "Miriam" }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.put(f'/user/{regular_user.id}', headers=headers, json=user_details)
    assert response.json['message'] == "Unauthorized user"
    assert response.status_code==401

def test_delete_user(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.delete(f'/user/{user.id}', headers=headers)
    assert response.json['message']
    assert response.status_code==200

def test_delete_user_for_user_not_found(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.delete('/user/200', headers=headers)
    assert response.json['message'] == "User not found"
    assert response.status_code==404

def test_delete_user_for_unauthorized_user(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": "test_user",
                "email": "test_user@gmail.com",
                "password": "password"
            })
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.delete(f'/user/{regular_user.id}', headers=headers)
    assert response.json['message'] == "Unauthorized User"
    assert response.status_code==401

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
    assert len(response_body['users']) == 6
    assert response.status_code==200

def test_super_admin_for_user_get_user(client, create_super_user_jwt_token, create_user):
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password"
            })
    response = client.get(f'/admin/user/{regular_user.id}', headers=headers)
    response_body = response.json
    assert response_body['email']=='test_user@gmail.com'
    assert response_body['username']=='test_user'
    assert response.status_code==200

def test_admin_for_user_get_user_details(client, create_admin_jwt_token, create_user):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password"
            })
    response = client.get(f'/admin/user/{regular_user.id}', headers=headers)
    response_body = response.json
    assert response_body['email']=='test_user@gmail.com'
    assert response_body['username']=='test_user'
    assert response.status_code==200

def test_admin_for_user_get_user_tourist_details(client, 
                                                create_admin_jwt_token,
                                                create_tourist, create_user):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password"
            })
    create_tourist(user=regular_user)
    response = client.get(f'/admin/user/{regular_user.id}', headers=headers)
    response_body = response.json
    assert response_body['user_detail']['email']=='test_user@gmail.com'
    assert response_body['user_detail']['username']=='test_user'
    assert response_body['tourist_id']
    assert response.status_code==200

def test_super_admin_for_user_get_user_details(client, create_super_user_jwt_token, create_user):
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password"
            })
    response = client.get(f'/admin/user/{regular_user.id}', headers=headers)
    response_body = response.json
    assert response_body['email']=='test_user@gmail.com'
    assert response_body['username']=='test_user'
    assert response.status_code==200

def test_super_admin_for_user_get_user_tourist_details(client, 
                                                create_super_user_jwt_token,
                                                create_tourist, create_user):
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password"
            })
    create_tourist(user=regular_user)
    response = client.get(f'/admin/user/{regular_user.id}', headers=headers)
    response_body = response.json
    assert response_body['user_detail']['email']=='test_user@gmail.com'
    assert response_body['user_detail']['username']=='test_user'
    assert response_body['tourist_id']
    assert response.status_code==200

def test_super_admin_for_get_user_does_not_exist(client, create_super_user_jwt_token):
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.get('/admin/user/200', headers=headers)
    assert response.status_code==404
    assert response.json['message'] == "User not found"

def test_admin_for_get_user_does_not_exist(client, create_admin_jwt_token):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.get('/admin/user/200', headers=headers)
    assert response.status_code==404
    assert response.json['message'] == "User not found"

def test_admin_for_get_user_authorized(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    regular_user = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password"
            })
    response = client.get(f'/admin/user/{regular_user.id}', headers=headers)
    assert response.status_code==401
    assert response.json['message'] == "Unauthorized User"

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
    assert len(response_body['users']) == 6
    assert response.status_code==200

def test_non_admin_get_users_list(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()

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
    assert response.status_code==401
    assert response_body['message'] == "Unauthorized User"

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

def test_for_only_super_admin_can_add_user(client, create_admin_jwt_token):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    user_detail = {"last_name": "Test",
                "first_name": "User",
                "username": "new_user",
                "email": "new_user@gmail.com",
                "password": "password"}
    response = client.post('/admin/user', headers=headers, json=user_detail)
    assert response.status_code==401
    assert response.json['message']=="Only Super Admins are allowed"

def test_for_only_super_admin_user_already_exist(client, create_user,
                                         create_super_user_jwt_token):
    create_user()
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    user_details = {
                "last_name": "Stone",
                "first_name": "Mark",
                "username": "stone",
                "email": "stone@gmail.com",
                "password": "stone"
            }
    response = client.post('/admin/user', headers=headers, json=user_details)
    assert response.status_code==400
    assert response.json['message'] == "User already exist"

def test_for_only_super_admin_username_already_exist(client, create_user,
                                         create_super_user_jwt_token):
    create_user()
    user, access_token = create_super_user_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    user_details = {
                "last_name": "Stone",
                "first_name": "Mark",
                "username": "stone",
                "email": "stone2000@gmail.com",
                "password": "stone"
            }
    response = client.post('/admin/user', headers=headers, json=user_details)
    assert response.status_code==400
    assert response.json['message'] == "Username already exist"

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

def test_only_super_admin_can_edit_user(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()
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
    assert response.json['message'] == "Only Super Admins are allowed"

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

def test_admin_delete_inactive_user(client, create_admin_jwt_token):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.delete('/admin/user/200', headers=headers)
    assert response.json['message'] == "User does not exist"
    assert response.status_code==404

def test_admin_delete_for_unauthorized_user(client, create_jwt_token, create_user):
    user, access_token = create_jwt_token()
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
    assert response.json['message'] == "Unauthorized User"
    assert response.status_code==401

def test_admin_delete_another_admin(client, create_admin_jwt_token, create_user):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    users = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password",
                "role_id": 2
            })
    response = client.delete(f'/admin/user/{users.id}', headers=headers)
    assert response.json['message'] == "Admin cannot delete self or other Admins"
    assert response.status_code==400

def test_admin_delete_super_admin(client, create_admin_jwt_token, create_user):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    users = create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user",
                "email": f"test_user@gmail.com",
                "password": "password",
                "role_id": 1
            })
    response = client.delete(f'/admin/user/{users.id}', headers=headers)
    assert response.json['message'] == "Admin cannot delete SuperAdmin"
    assert response.status_code==400

def test_token_refresh(client, create_refresh_jwt_token):
    user, refresh_token = create_refresh_jwt_token()
    headers = {"Authorization":f"Bearer {refresh_token}"}
    response = client.post('/refresh', headers=headers)
    assert response.status_code==200
