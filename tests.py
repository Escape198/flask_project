from app import client
from models import Message


def test_get():
    res = client.get('/message')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Message.query.all())
    #assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'messages': 'Unit Tests',
    }

    res = client.post('/message', json=data)

    assert res.status_code == 200

'''
def test_put():
    res = client.put('/message/1', json={'message': 'UPD'})

    assert res.status_code == 200
    assert Message.query.get(1).message == 'UPD'


def test_delete():
    res = client.delete('/message/1')

    assert res.status_code == 204
    assert Message.query.get(1) is None
'''
