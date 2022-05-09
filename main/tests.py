from app import client
from models import Message


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjA0NzQ5NSwianRpIjoiZjE0ZWNhN2EtNDc2ZS00MmY3LTkxMDMtMTEwMDBjNDNiZWQ2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjUyMDQ3NDk1LCJleHAiOjE2NTQxMjEwOTV9.PPdjJMUoem2XtcqjH-ZrXc6229PYAaoYoqwA8aMj00E'
headers = {'Authorization': f'Bearer {token}',
'Content-Type': 'application/json'}


def test_post():
    data = {
        'messages': 'Unit Tests'
        }

    res = client.post('api/v1/message', json=data, headers=headers)

    assert res.status_code == 200

def test_get():
    res = client.get('api/v1/message', headers=headers)

    assert res.status_code == 200
    assert len(res.get_json()) == len(Message.query.all())
