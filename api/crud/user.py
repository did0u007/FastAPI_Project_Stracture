from typing import Annotated
from fastapi import Form, HTTPException, UploadFile, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from api.core.helper import raise_error
from api.models.user import User
from api.schemas.user import UserRequest
from api.crud import file as fl
from sqlalchemy.exc import IntegrityError
from api.core.helper import integrety_error_hundler as ieh


async def get_user_depends(
    username: Annotated[str, Form],
    email: Annotated[str, Form],
    password: Annotated[str, Form],
    confirmed_password: Annotated[str, Form],
    state_id: Annotated[int, Form],
    name: Annotated[str | None, Form] = None,
    address: Annotated[str | None, Form] = None,
    phone: Annotated[str | None, Form] = None,
    city_id: Annotated[int | None, Form] = None,
) -> UserRequest:
    try:
        return UserRequest(**locals())
    except ValidationError as e:
        raise RequestValidationError(e.errors())
    # return {key: value for key, value in locals().items() if value is not None}


############### Create New User #################


async def db_ceate_user(db: Session, user: UserRequest, img=None):
    db_user = User(**user.model_dump())
    try:
        # type: ignore
        db.add(db_user)
        if img is not None:
            user_img = await fl.db_upload_file(db, img, is_public=True)
            db_user.profile_img = user_img.get("id")  # type: ignore
        db.flush([db_user])
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise_error(status.HTTP_409_CONFLICT, ieh(e.orig))  # TODO: handle exception

    return db_user
