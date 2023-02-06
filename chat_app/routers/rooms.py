from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.rooms import schemas
from chat_app.services import room_service
from chat_app.users import schemas as users_schemas
from chat_app.users import crud as users_crud


router = APIRouter()


@router.post('/user/room', response_model=users_schemas.User)
async def add_room(*,
                   room: schemas.Room,
                   db: Session = Depends(dependencies.get_db)):
    db_user = users_crud.get_user_by_username(db=db, username=room.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user')
    return room_service.add_room(
        db=db, username=room.username, room=room.room)


@router.delete('/user/room', response_model=users_schemas.User)
async def remove_room(*,
                      room: schemas.Room,
                      db: Session = Depends(dependencies.get_db)):
    db_user = users_crud.get_user_by_username(db=db, username=room.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user')
    return room_service.remove_room(
        db=db, username=room.username, room=room.room)
