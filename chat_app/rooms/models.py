from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from chat_app.database import Base


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
