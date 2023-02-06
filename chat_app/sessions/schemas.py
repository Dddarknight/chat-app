from pydantic import BaseModel


class Session(BaseModel):
    username: str
    sid: str
