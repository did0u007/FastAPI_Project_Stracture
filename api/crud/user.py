from typing import Annotated
from fastapi import Body
from sqlalchemy.orm import Session
from api.models.user import User
from api.schemas.user import UserRequest


async def db_ceate_user(db: Session, user: UserRequest):
    user = User(**user.model_dump())  # type: ignore
    return user
