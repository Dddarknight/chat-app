from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from chat_app.messages.models import Message
from chat_app.messages.schemas import MessageCreate


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).offset(skip).limit(limit).all()


def get_message(db: Session, id: int):
    return db.query(Message).filter(Message.id == id).first()


def create_message(db: Session,
                   message: MessageCreate,
                   user_id: int):
    db_message = Message(content=message.content, author_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_db_message(db: Session,
                      message_id: int,
                      new_message_data: Union[BaseModel, Dict[str, Any]]):
    db_message = get_message(db, message_id)
    db_message_data = jsonable_encoder(db_message)
    if isinstance(new_message_data, dict):
        update_data = new_message_data
    else:
        update_data = new_message_data.dict(exclude_unset=True)
    for field in db_message_data:
        if field in update_data:
            setattr(db_message, field, update_data[field])
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session,
                   message_id: int):
    db_message = get_message(db, message_id)
    db.delete(db_message)
    db.commit()
    return db_message
