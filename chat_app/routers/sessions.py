from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.sessions import schemas
from chat_app.services import session_service
from chat_app.users import schemas as users_schemas
from chat_app.users import crud as users_crud


router = APIRouter()


@router.post('/user/sid', response_model=users_schemas.User)
async def set_session_id(*,
                         sid: schemas.Session,
                         db: Session = Depends(dependencies.get_db)):
    db_user = users_crud.get_user_by_username(db=db, username=sid.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user')
    return session_service.set_session_id(
        db=db, username=sid.username, session_id=sid.sid)
