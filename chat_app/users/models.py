from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from chat_app.database import Base
from chat_app.rooms.models import UserRoom


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
