
def test_list(message, client, user_headers):
    res = client.get('/api/v1/message', headers=user.heders)

    assert res.status_code == 200
