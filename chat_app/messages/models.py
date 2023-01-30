import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship

from chat_app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    room = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    author = relationship("User", back_populates="messages")
    like = relationship("Like", uselist=False, back_populates="message")


UserRoom = Table('UserRoom',
                 Base.metadata,
                 Column('user_id', ForeignKey('users.id')),
                 Column('room_id', ForeignKey('rooms.id')))


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String)
    users = relationship(
        "User", secondary=UserRoom, back_populates="rooms"
    )


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=1)
    message_id = Column(Integer, ForeignKey("messages.id"))

    message = relationship("Message", back_populates="like")
