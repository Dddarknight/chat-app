import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chat_app.server import app
from chat_app.database import Base
from chat_app.dependencies import get_db
from chat_app.tests.utils import get_test_data
from chat_app.tests.test_users import test_data_users
from chat_app.services import auth_service


test_data_messages = get_test_data('messages.json')

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


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


def test_create_and_get_message(test_db):
    user_data = test_data_users["users"]["user1"]
    client.post('/sign-up', json=user_data)

    message_data = test_data_messages["messages"]["message1"]

    sid = message_data['sid']
    sid_data = {'username': user_data['username'], 'sid': sid}
    client.post('/user/sid', json=sid_data)

    db_user = auth_service.authenticate_user(
        TestingSessionLocal(),
        test_data_users["users"]["user1"]["username"],
        test_data_users["users"]["user1"]["password"])
    access_token = auth_service.get_access_token(db_user)

    message = client.post('/create-message',
                          json=message_data,
                          headers={"Authorization": f"Bearer {access_token}"})
    assert message.json()['content'] == message_data['content']

    messages = client.get('/messages',
                          headers={"Authorization": f"Bearer {access_token}"})
    for message in messages.json():
        assert message['content'] == message_data['content']
