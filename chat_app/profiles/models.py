from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from chat_app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary)
    thumbnail_50 = Column(LargeBinary)
    thumbnail_100 = Column(LargeBinary)
    thumbnail_400 = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")
