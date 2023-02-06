from pydantic import BaseModel


class Room(BaseModel):
    username: str
    room: str


class DbRoom(BaseModel):
    id: int
    room_number: str

    class Config:
        orm_mode = True
