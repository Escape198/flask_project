from app import client


def test_simple():
    mylist = [1, 2, 3, 4, 5]

    assert 1 in mylist


def test_get():
    res = client.get('/message')

    assert res.status_code == 200

    assert len(res.get_json()) == 2
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'id': 3,
        'title': 'Unit Tests',
        'text': 'Pytest message'
    }

    res = client.post('/message', json=data)

    assert res.status_code == 200

    assert len(res.get_json()) == 3
    assert res.get_json()[-1]['text'] == data['text']

