import pytest
import sys

sys.path.append('..')


from main import  app
from main import Base, engine, session as db_session
from main.models import User, Message


@pytest.fixture(scope='function')
def testapp():
    _app = app

    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()

@pytest.fixture(scope='function')
def session(testapp):
    ctx = app.app_context()
    ctx.push()

    yield db_session

    db_session.close_all()
    ctx.pop()

@pytest.fixture(scope='function')
def user(session):
    user = User(
        name = 'Testuser',
        email = 'test@test.com',
        password = 'password'
    )
    session.add(user)
    session.commit()

    return user

@pytest.fixture
def client(testapp):
    return testapp.test_client()

@pytest.fixture
def user_token(user, client):
    res = client.post('/auth',json={
        'email': user.email,
        'password': 'password'
    })
    return res.get_json()['access_token']

@pytest.fixture
def user_headers(user_token):
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    return headers

@pytest.fixture
def message(user, session):
    message = Message(
        user_id=user_id,
        name='Message 1',
        status='review'
    )
    session.add(message)
    session.commit()
    return message
