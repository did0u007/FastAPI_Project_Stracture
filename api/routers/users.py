from typing import Annotated
from fastapi import APIRouter, Depends, File, Path, Query, UploadFile
from api.db import getDB
from api.schemas import UserRequest
from sqlalchemy.orm import Session
from api.crud import user as us
from api.schemas import UserResponse


router = APIRouter(prefix="/user", tags=["user"])


############## Create User #####################
@router.post("/create", response_model=UserResponse)
async def create_user(
    user: Annotated[UserRequest, Depends(us.get_user_depends)],
    db: Session = Depends(getDB),
    profile_img: UploadFile = File(default=None),
):
    return await us.db_ceate_user(db, user, profile_img)


####################### ADMIN PRIVLEGE ONLY #################
# TODO: Add check for admin only. middleware here.
@router.get("/{id}", tags=["admin"])
async def get_user_by_id(id: int):
    print("on")
    return {"test": f"passed {id}"}


@router.get("/{id}/delete", tags=["admin"])
async def drope_user(
    id: Annotated[int, Path],
    soft: Annotated[bool, Query] = True,
    db: Session = Depends(getDB),
):
    return await us.db_drope_user(db, id, soft)
