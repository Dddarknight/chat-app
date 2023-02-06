from sqlalchemy.orm import Session

from chat_app.likes.models import Like
from chat_app.likes.schemas import LikeCreate


def get_like_by_msg_id(db: Session, id: int):
    return db.query(Like).filter(Like.message_id == id).first()


def add_like(db: Session,
             like: LikeCreate):
    db_like = get_like_by_msg_id(db, like.message_id)
    if not db_like:
        db_like = Like(message_id=like.message_id)
    else:
        db_like.count += 1
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like
