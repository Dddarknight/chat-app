from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from chat_app.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=1)
    message_id = Column(Integer, ForeignKey("messages.id"))

    message = relationship("Message", back_populates="like")
