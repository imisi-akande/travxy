def test_get_role(client, create_admin_jwt_token, create_user):
    user, access_token = create_admin_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    create_user()
    response = client.get("/roles", headers=headers)
    assert response.status_code==200

def test_get_role_for_unauthorized_user(client, create_jwt_token):
    user, access_token = create_jwt_token()
    headers = {"Authorization":f"Bearer {access_token}"}
    response = client.get("/roles", headers=headers)
    assert response.status_code==401


