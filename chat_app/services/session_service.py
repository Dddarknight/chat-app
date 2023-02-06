from sqlalchemy.orm import Session

from chat_app.users.models import User


def set_session_id(db: Session, username: str, session_id: str):
    db_user = db.query(User).filter(User.username == username).first()
    db_user.session_id = session_id
    db.commit()
    return db_user
