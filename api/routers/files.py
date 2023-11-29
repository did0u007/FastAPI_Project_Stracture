from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, Response, UploadFile, File
from sqlalchemy.orm import Session

from api.db import getDB
from api.schemas import UploadResponse
from api.crud import file as fl

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/get-file/{filename}")
async def get_file(
    filename: Annotated[str, Path],
    db: Session = Depends(getDB),
):
    return await fl.db_get_file(db, filename)
    ...
