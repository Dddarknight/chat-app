from typing import Union, List

from pydantic import BaseModel

from chat_app.rooms.schemas import DbRoom


class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    session_id: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    rooms: List[DbRoom]

    class Config:
        orm_mode = True
