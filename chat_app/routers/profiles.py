import base64

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from chat_app import dependencies
from chat_app.profiles import schemas, crud
from chat_app.routers.utils import get_image_value


router = APIRouter()


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
