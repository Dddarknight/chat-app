from typing import Optional

from pydantic import BaseModel


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
