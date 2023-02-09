from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.messages import repo, schemas
from chat_app.users import repo as users_repo


router = APIRouter()


@router.get("/messages", response_model=List[schemas.Message])
async def read_messages(db: Session = Depends(dependencies.get_db),
                        skip: int = 0,
                        limit: int = 100):
    return repo.get_messages(db=db, skip=skip, limit=limit)


@router.post('/create-message', response_model=schemas.Message)
async def create_message(*,
                         message: schemas.MessageCreate,
                         db: Session = Depends(dependencies.get_db)):
    db_user = users_repo.get_user_by_session_id(db=db, session_id=message.sid)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user.')
    return repo.create_message(db=db, message=message, user_id=db_user.id)
