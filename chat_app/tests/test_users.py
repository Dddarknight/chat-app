import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chat_app.server import app
from chat_app.database import Base
from chat_app.dependencies import get_db
from chat_app.tests.utils import get_test_data
from chat_app.services import auth_service


test_data_users = get_test_data('users.json')

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user(test_db):
    data = test_data_users["users"]["user1"]
    user = client.post('/sign-up',
                       json=data)
    assert user.json()['username'] == data['username']
    assert user.json()['email'] == data['email']
    assert user.json()['full_name'] == data['full_name']


def test_get_user(test_db):
    data = test_data_users["users"]["user1"]
    client.post('/sign-up', json=data)
    user = client.get('/users/1')
    assert user.json()['username'] == data['username']
    assert user.json()['email'] == data['email']
    assert user.json()['full_name'] == data['full_name']


def test_update_user(test_db):
    data_initial = test_data_users["users"]["user1"]
    user = client.post('/sign-up', json=data_initial)
    db_user = auth_service.authenticate_user(
        TestingSessionLocal(),
        test_data_users["users"]["user1"]["username"],
        test_data_users["users"]["user1"]["password"])
    access_token = auth_service.get_access_token(db_user)
    data_changed = test_data_users["users"]["user2"]
    user = client.put('/users/1',
                      json=data_changed,
                      headers={"Authorization": f"Bearer {access_token}"})
    assert user.json()['username'] == data_changed['username']
    assert user.json()['email'] == data_changed['email']
    assert user.json()['full_name'] == data_changed['full_name']


def test_delete_user(test_db):
    data = test_data_users["users"]["user1"]
    client.post('/sign-up', json=data)
    db_user = auth_service.authenticate_user(
        TestingSessionLocal(),
        test_data_users["users"]["user1"]["username"],
        test_data_users["users"]["user1"]["password"])
    access_token = auth_service.get_access_token(db_user)
    client.delete('/users/1',
                  headers={"Authorization": f"Bearer {access_token}"})
    response = client.get('/users/1')
    assert response.status_code == 404


def test_add_sid(test_db):
    data = test_data_users["users"]["user1"]
    client.post('/sign-up', json=data)
    sid = '12345'
    sid_data = {'username': data['username'], 'sid': sid}
    user = client.post('/user/sid', json=sid_data)
    assert user.json()['username'] == data['username']
    assert user.json()['email'] == data['email']
    assert user.json()['full_name'] == data['full_name']
    assert user.json()['session_id'] == sid


def test_add_and_delete_room(test_db):
    data = test_data_users["users"]["user1"]
    client.post('/sign-up', json=data)
    room = '12'
    room_data = {'username': data['username'], 'room': room}
    user = client.post('/user/room', json=room_data)
    assert user.json()['username'] == data['username']
    assert user.json()['email'] == data['email']
    assert user.json()['full_name'] == data['full_name']
    assert user.json()['rooms'] == [{'id': 1, 'room_number': '12'}]
