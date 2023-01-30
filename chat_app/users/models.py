from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from chat_app.database import Base
from chat_app.messages.models import UserRoom


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    session_id = Column(String)

    messages = relationship("Message", back_populates="author")
    rooms = relationship(
        "Room", secondary=UserRoom, back_populates="users"
    )
    profile = relationship("Profile", uselist=False, back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary)
    thumbnail_50 = Column(LargeBinary)
    thumbnail_100 = Column(LargeBinary)
    thumbnail_400 = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")
