from fastapi import UploadFile
from sqlalchemy.orm import Session
from api.models.user import User
from api.schemas.user import UserRequest
from api.crud import file as fl


async def db_ceate_user(db: Session, user: UserRequest, img: UploadFile | None):
    # user_data = user.model_dump()
    # user_data.pop("confirmed_password", None)
    if img is not None:
        profile_img = await fl.db_upload_file(img, db, is_public=True)
    user = User(**user.model_dump())  # type: ignore
    return user
