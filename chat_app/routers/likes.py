from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.likes import repo, schemas
from chat_app.messages import repo as messages_repo


router = APIRouter()


@router.post('/like', response_model=schemas.Like)
async def add_like(*,
                   like: schemas.LikeCreate,
                   db: Session = Depends(dependencies.get_db)):
    db_message = messages_repo.get_message(db=db, id=like.message_id)
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such message.')
    return repo.add_like(db=db, like=like)
