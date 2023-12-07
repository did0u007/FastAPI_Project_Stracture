from typing import Annotated
from fastapi import APIRouter, Body, Depends, UploadFile
from api.db import getDB
from api.models import User
from api.schemas import UserResponse, UserRequest
from sqlalchemy.orm import Session
from api.crud import user as us


router = APIRouter(prefix="/user", tags=["user"])


############## Create User #####################
@router.post("/create")
async def create_user(
    user: Annotated[UserRequest, Body],
    db: Session = Depends(getDB),
    img: UploadFile | None = None,
):
    return await us.db_ceate_user(db, user, img)


####################### ADMIN PRIVLEGE ONLY #################
# TODO: Add check for admin only. middleware here.
@router.get("/{id}", tags=["admin"])
async def get_user_by_id(id: int):
    print("on")
    return {"test": f"passed {id}"}
