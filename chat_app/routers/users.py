from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.users import schemas, crud


router = APIRouter()


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
