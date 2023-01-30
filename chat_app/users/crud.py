from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from chat_app.users.models import User, Profile
from chat_app.users.schemas import UserCreate, ProfileCreate
from chat_app.messages.models import Room


def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session,
                      username: str,
                      password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session,
                user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username,
                   email=user.email,
                   full_name=user.full_name,
                   hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session,
                user_id: int,
                new_user_data: Union[BaseModel, Dict[str, Any]]):
    db_user = get_user(db, user_id)
    db_user_data = jsonable_encoder(db_user)
    if isinstance(new_user_data, dict):
        update_data = new_user_data
    else:
        update_data = new_user_data.dict(exclude_unset=True)
    for field in db_user_data:
        if field in update_data:
            if field == 'password':
                update_data[field] = get_password_hash(update_data[field])
            setattr(db_user, field, update_data[field])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session,
                user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def set_session_id(db: Session, username: str, session_id: str):
    db_user = db.query(User).filter(User.username == username).first()
    db_user.session_id = session_id
    db.commit()
    return db_user


def get_user_by_session_id(db: Session, session_id: str):
    db_user = db.query(User).filter(User.session_id == session_id).first()
    return db_user


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


def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_profile(db: Session,
                   profile: ProfileCreate,
                   image: bytes,
                   thumbnail_50: bytes,
                   thumbnail_100: bytes,
                   thumbnail_400: bytes):
    db_profile = Profile(image=image,
                         thumbnail_50=thumbnail_50,
                         thumbnail_100=thumbnail_100,
                         thumbnail_400=thumbnail_400,
                         user_id=profile.user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profile(db: Session, id: int):
    return db.query(Profile).filter(Profile.id == id).first()
