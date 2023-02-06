from sqlalchemy.orm import Session

from chat_app.profiles.models import Profile
from chat_app.profiles.schemas import ProfileCreate


def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_profile(db: Session,
                   profile: ProfileCreate,
                   image: bytes,
                   thumbnail_50: bytes,
                   thumbnail_100: bytes,
                   thumbnail_400: bytes):
    db_profile = Profile(image=image,
                         thumbnail_50=thumbnail_50,
                         thumbnail_100=thumbnail_100,
                         thumbnail_400=thumbnail_400,
                         user_id=profile.user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profile(db: Session, id: int):
    return db.query(Profile).filter(Profile.id == id).first()
