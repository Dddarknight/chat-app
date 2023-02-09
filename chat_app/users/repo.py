from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from chat_app.users.models import User
from chat_app.users.schemas import UserCreate
from chat_app.services import auth_service


def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_session_id(db: Session, session_id: str):
    db_user = db.query(User).filter(User.session_id == session_id).first()
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session,
                user: UserCreate):
    hashed_password = auth_service.get_password_hash(user.password)
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
                update_data[field] = auth_service.get_password_hash(
                    update_data[field])
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
