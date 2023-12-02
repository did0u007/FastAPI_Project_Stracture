from typing import Annotated
from fastapi import Body
from sqlalchemy.orm import Session
from api.models.user import User
from api.schemas.user import UserRequest


async def db_ceate_user(db: Session, user: UserRequest):
    user_data = user.model_dump()
    user_data.pop("confirmed_password", None)
    user = User(**user_data)  # type: ignore
    return user
