import pytest
from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chat_app.server import app
from chat_app.database import Base
from chat_app.dependencies import get_db
from chat_app.tests.utils import get_test_data
from chat_app.tests.test_users import test_data_users
from chat_app.tokens.token import create_access_token


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
    user = client.post('/sign-up', json=user_data)

    message_data = test_data_messages["messages"]["message1"]

    sid = message_data['sid']
    sid_data = {'username': user_data['username'], 'sid': sid}
    user = client.post('/user/sid', json=sid_data)

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.json()['username']},
        expires_delta=access_token_expires
    )

    message = client.post('/create-message',
                          json=message_data,
                          headers={"Authorization": f"Bearer {access_token}"})
    assert message.json()['content'] == message_data['content']

    messages = client.get('/messages',
                          headers={"Authorization": f"Bearer {access_token}"})
    print(messages)
    for message in messages.json():
        assert message['content'] == message_data['content']
