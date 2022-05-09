

def test_model(user):
    assert user.name == 'Testuser'

def test_user_auth(user, client):
    res = client.post('/auth',json={
        'email': user.email,
        'password': 'password'
    })
    assert res.status_code == 200
    assert res.get_json().get('access_token')

def test_user_registration(client):
    res = client.post('/sign_up',json={
        'name': 'Testuser',
        'email': 'test@test.com',
        'password': 'password'
    })
    assert res.status_code == 200
    #assert res.get_json()
