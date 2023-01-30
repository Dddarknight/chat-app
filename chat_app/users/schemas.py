from typing import Union, List, Optional

from pydantic import BaseModel

from chat_app.messages.schemas import Room


class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    session_id: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    rooms: List[Room]

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    pass


class ProfileCreate(ProfileBase):
    user_id: int


class Profile(ProfileBase):
    id: int
    user_id: int
    image: Optional[str] = None

    class Config:
        orm_mode = True


class Session(BaseModel):
    username: str
    sid: str


class Room(BaseModel):
    username: str
    room: str
