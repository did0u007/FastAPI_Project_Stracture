from typing import List
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from api.db.database import get_db

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload_files(
    file: List[UploadFile],
    db: Session = Depends(get_db),
):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }
