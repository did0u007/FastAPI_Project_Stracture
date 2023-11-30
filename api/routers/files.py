from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from api.crud import file as fl
from fastapi import APIRouter, Depends, Path
from typing import Annotated, List
from api.db import getDB

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/get-file/{filename}", response_model=HTMLResponse)
async def get_file(
    filename: Annotated[str, Path],
    db: Session = Depends(getDB),
):
    return await fl.db_get_file(db, filename)  # type: ignore
    ...
