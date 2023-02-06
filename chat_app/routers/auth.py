from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.services import auth_service
from chat_app.tokens.models import Token


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        db: Session = Depends(dependencies.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):

    user = auth_service.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.get_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
