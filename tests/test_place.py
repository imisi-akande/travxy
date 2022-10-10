def test_get_place(client, create_jwt_token, create_tourist, create_place):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    create_tourist(user=user)
    places = [create_place({
                "name": f"Place{i}",
                "location": f"location{i}",
                "country": f"country{i}",
                "about": f"about{i}"
            }) for i in range(3)]
    response = client.get("/places", headers=headers)
    assert response.status_code==200
    assert len(response.json['results']) == 3