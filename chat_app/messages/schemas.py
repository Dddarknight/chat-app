from typing import Union, List
from datetime import datetime

from pydantic import BaseModel


class LikeBase(BaseModel):
    message_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    count: int

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    content: Union[str, None] = None
    room: Union[str, None] = None


class MessageCreate(MessageBase):
    sid: Union[str, None] = None


class Message(MessageBase):
    id: int
    author_id: int
    created_at: datetime = None

    class Config:
        orm_mode = True


class Room(BaseModel):
    id: int
    room_number: str

    class Config:
        orm_mode = True
