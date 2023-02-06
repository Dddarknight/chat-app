from sqlalchemy.orm import Session

from chat_app.users.models import User
from chat_app.rooms.models import Room


def add_room(db: Session, username: str, room: str):
    db_user = db.query(User).filter(User.username == username).first()
    db_room = db.query(Room).filter(Room.room_number == room).first()
    if not db_room:
        db_room = Room(room_number=room)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    db_user.rooms.append(db_room)
    db.commit()
    return db_user


def remove_room(db: Session, username: str, room: str):
    db_user = db.query(User).filter(User.username == username).first()
    db_room = db.query(Room).filter(Room.room_number == room).first()
    db_user.rooms.remove(db_room)
    db.commit()
    return db_user
