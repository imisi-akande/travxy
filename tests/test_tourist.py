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
