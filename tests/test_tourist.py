def test_register_tourist(client, create_jwt_token):
    user, access_token = create_jwt_token()
    tourist_details = {
        "nationality": "Australia",
        "gender": "Male"
    }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.post('/tourists', json=tourist_details, headers=headers)
    assert response.status_code==201
    assert response.json['tourist_id']

def test_register_tourist_missing_fields(client, create_jwt_token):
    user, access_token = create_jwt_token()
    tourist_details = {
        "gender": "Male"
    }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.post('/tourists', json=tourist_details, headers=headers)
    assert response.status_code==400
    assert response.json['message']

def test_get_tourist_list(client, create_jwt_token, create_user,
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
            }) for i in range(4)]
    for usr in users:
        create_tourist(user=usr)
    response = client.get('/tourists', headers=headers)
    assert response.status_code==200
    assert len(response.json['tourists']) == 5

def test_non_tourist_get_tourist_list(client, create_jwt_token, create_user,
                    create_tourist):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}

    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(2)]
    for usr in users:
        create_tourist(user=usr)
    response = client.get('/tourists', headers=headers)
    assert response.status_code==400
    assert response.json['message']

def test_get_tourist(client, create_jwt_token, create_user,
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
    test_user = users[1]
    response = client.get(f"/tourist/{test_user.id}", headers=headers)
    assert response.status_code==200
    assert response.json['tourist_id']

def test_get_tourist_for_non_tourist_user(client, create_jwt_token, create_user,
                    create_tourist):
    user, access_token = create_jwt_token()

    headers = {"Authorization":f"Bearer {access_token}"}
    users = [create_user({
                "last_name": "Test",
                "first_name": "User",
                "username": f"test_user{i}",
                "email": f"test_user{i}@gmail.com",
                "password": "password"
            }) for i in range(2)]
    for usr in users:
        create_tourist(user=usr)
    test_user = users[1]
    response = client.get(f"/tourist/{test_user.id}", headers=headers)
    assert response.status_code==400
    assert response.json['message']

def test_get_tourist_for_inactive_tourist(client, create_jwt_token, create_user,
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
    response = client.get(f'/tourist/{regular_user.id}', headers=headers)
    assert response.status_code==404
    assert response.json['message']

def test_edit_tourist(client, create_jwt_token, create_tourist):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    tourist_details = {
                "nationality": "India",
                "gender": "Male",
            }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.put(f'/tourist/{user.id}', headers=headers,
                            json=tourist_details)
    assert response.status_code==200

def test_edit_tourist_not_a_registered_tourist(client, create_jwt_token, create_tourist):
    user, access_token = create_jwt_token()
    tourist_details = {
                "nationality": "India",
                "gender": "Male",
            }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.put(f'/tourist/{user.id}', headers=headers,
                            json=tourist_details)
    assert response.status_code==400
    assert response.json['message']

def test_edit_tourist_different_tourist_id(client, create_jwt_token, create_tourist):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    tourist_details = {
                "nationality": "India",
                "gender": "Male",
            }
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.put('/tourist/3', headers=headers,
                            json=tourist_details)
    assert response.status_code==401
    assert response.json['message']

def test_add_tourist_details(client, create_jwt_token, create_tourist,
                            create_detail):
    user, access_token = create_jwt_token()
    create_tourist(user=user)

    create_detail()

    place_details = {"place_id": 1,
                    "departure": "Austria",
                    "transportation": "Air",
                    "travel_buddies": ['test_user1@gmail.com', 'test_user2@gmail.com'],
                    "estimated_cost": 2500}
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/tourist-details', headers=headers,
                            json=place_details)
    assert response.status_code==201

def test_add_tourist_details_for_missing_fields(client, create_jwt_token,
                                            create_tourist, create_detail):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    create_detail()
    place_details = {"place_id": 1,
                    "departure": "Austria",
                    "travel_buddies": ['test_user1@gmail.com', 'test_user2@gmail.com'],
                    "estimated_cost": 2500}
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/tourist-details', headers=headers,
                            json=place_details)
    assert response.status_code==400
    assert response.json['message']

def test_add_tourist_details_for_place_non_exist(client, create_jwt_token,
                                            create_tourist, create_detail):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    create_detail()
    place_details = {"place_id": 100,
                    "departure": "Austria",
                    "transportation": "Air",
                    "travel_buddies": ['test_user0@gmail.com',
                                        'test_user1@gmail.com', 'test_user2@gmail.com'],
                    "estimated_cost": 2500}
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/tourist-details', headers=headers,
                            json=place_details)
    assert response.status_code==400
    assert response.json['message']

def test_add_tourist_details_for_non_tourist(client, create_jwt_token,
                                            create_tourist, create_detail):
    user, access_token = create_jwt_token()
    create_detail()
    place_details = {"place_id": 1,
                    "departure": "Austria",
                    "transportation": "Air",
                    "travel_buddies": ['test_user0@gmail.com',
                                       'test_user1@gmail.com', 'test_user2@gmail.com'],
                    "estimated_cost": 2500}
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/tourist-details', headers=headers,
                            json=place_details)
    assert response.status_code==401
    assert response.json['message']

def test_add_tourist_details_for_adding_author_to_buddies(client, create_jwt_token,
                                            create_tourist, create_detail):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    create_detail()
    place_details = {"place_id": 1,
                    "departure": "Austria",
                    "transportation": "Air",
                    "travel_buddies": ['stone@gmail.com', 'test_user0@gmail.com',
                                        'test_user1@gmail.com', 'test_user2@gmail.com'],
                    "estimated_cost": 2500}
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/tourist-details', headers=headers,
                            json=place_details)
    assert response.status_code==400
    assert response.json['message']

def test_add_tourist_details_for_non_tourist_buddies(client, create_jwt_token,
                                            create_tourist, create_detail):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    create_detail()
    place_details = {"place_id": 1,
                    "departure": "Austria",
                    "transportation": "Air",
                    "travel_buddies": ['test_user00@gmail.com',
                                       'test_user1@gmail.com', 'test_user2@gmail.com'],
                    "estimated_cost": 2500}
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.post('/tourist-details', headers=headers,
                            json=place_details)
    assert response.status_code==400
    assert response.json['message']

def test_get_tourist_details(client, create_jwt_token, create_tourist,
                            create_detail):
    user, access_token = create_jwt_token()
    create_tourist(user=user)
    create_detail()
    headers = {"Authorization":f"Bearer {access_token}"}

    response = client.get('/tourist-details', headers=headers)
    assert response.status_code==200
