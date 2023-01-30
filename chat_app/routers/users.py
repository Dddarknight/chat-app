import base64
from typing import List
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.tokens.models import Token
from chat_app.tokens.token import create_access_token
from chat_app.users import schemas, crud
from chat_app.routers.utils import get_image_value


ACCESS_TOKEN_EXPIRE_MINUTES = 360

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        db: Session = Depends(dependencies.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/", response_model=List[schemas.User])
async def read_users(db: Session = Depends(dependencies.get_db),
                     skip: int = 0,
                     limit: int = 100):
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(*,
                    user_id: int,
                    db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post('/sign-up', response_model=schemas.User)
async def create_user(*,
                      user: schemas.UserCreate,
                      db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered.')
    return crud.create_user(db=db, user=user)


@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(*,
                      user_id: int,
                      db: Session = Depends(dependencies.get_db),
                      new_user_data: schemas.UserCreate,
                      user: schemas.User = Depends(
                        dependencies.get_current_user)):
    db_user = crud.get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == user_id:
        return crud.update_user(db=db,
                                user_id=user_id,
                                new_user_data=new_user_data)
    raise HTTPException(status_code=404, detail="Can't update another user")


@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int,
                      db: Session = Depends(dependencies.get_db),
                      user: schemas.User = Depends(
                        dependencies.get_current_user),):
    db_user = crud.get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == user_id:
        return crud.delete_user(db=db,
                                user_id=user_id)
    raise HTTPException(status_code=404, detail="Can't delete another user")


@router.post('/create-profile', response_model=schemas.Profile)
async def create_profile(*,
                         user_id: str,
                         image: UploadFile,
                         db: Session = Depends(dependencies.get_db)):
    db_profile = crud.get_profile_by_user_id(db=db, user_id=user_id)
    if db_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already has the profile.')
    image_file_content = await image.read()
    image_bytes = base64.b64encode(image_file_content)
    thumbnail_50 = base64.b64encode(
        get_image_value(image_file_content, (50, 50))
    )
    thumbnail_100 = base64.b64encode(
        get_image_value(image_file_content, (100, 100))
    )
    thumbnail_400 = base64.b64encode(
        get_image_value(image_file_content, (400, 400))
    )
    return crud.create_profile(db=db,
                               profile=schemas.ProfileCreate(
                                   **{'user_id': user_id}),
                               image=image_bytes,
                               thumbnail_50=thumbnail_50,
                               thumbnail_100=thumbnail_100,
                               thumbnail_400=thumbnail_400)


@router.get("/profile/{profile_id}/original-image", response_class=Response)
async def get_user_image(*,
                         profile_id: int,
                         db: Session = Depends(dependencies.get_db)):
    db_profile = crud.get_profile(db=db, id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    image = base64.b64decode(db_profile.image)
    return Response(content=image, media_type='image/png')


@router.get("/profile/{profile_id}/thumbnail50", response_class=Response)
async def get_user_thumbnail_50(*,
                                profile_id: int,
                                db: Session = Depends(dependencies.get_db)):
    db_profile = crud.get_profile(db=db, id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    image = base64.b64decode(db_profile.thumbnail_50)
    return Response(content=image, media_type='image/png')


@router.get("/profile/{profile_id}/thumbnail100", response_class=Response)
async def get_user_thumbnail_100(*,
                                 profile_id: int,
                                 db: Session = Depends(dependencies.get_db)):
    db_profile = crud.get_profile(db=db, id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    image = base64.b64decode(db_profile.thumbnail_100)
    return Response(content=image, media_type='image/png')


@router.get("/profile/{profile_id}/thumbnail400", response_class=Response)
async def get_user_thumbnail_400(*,
                                 profile_id: int,
                                 db: Session = Depends(dependencies.get_db)):
    db_profile = crud.get_profile(db=db, id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    image = base64.b64decode(db_profile.thumbnail_400)
    return Response(content=image, media_type='image/png')


@router.post('/user/sid', response_model=schemas.User)
async def set_session_id(*,
                         sid: schemas.Session,
                         db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db=db, username=sid.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user')
    return crud.set_session_id(
        db=db, username=sid.username, session_id=sid.sid)


@router.post('/user/room', response_model=schemas.User)
async def add_room(*,
                   room: schemas.Room,
                   db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db=db, username=room.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user')
    return crud.add_room(
        db=db, username=room.username, room=room.room)


@router.delete('/user/room', response_model=schemas.User)
async def remove_room(*,
                      room: schemas.Room,
                      db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db=db, username=room.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No such user')
    return crud.remove_room(
        db=db, username=room.username, room=room.room)
