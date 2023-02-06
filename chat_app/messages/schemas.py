from typing import Union
from datetime import datetime

from pydantic import BaseModel


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
