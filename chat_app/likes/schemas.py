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
