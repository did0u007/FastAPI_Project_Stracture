from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from api.db.database import get_db

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload_files(
    file: List[UploadFile] = File(),
    db: Session = Depends(get_db),
):
    return [
        {
            "filename": f.filename,
            "content_type": f.content_type,
        }
        for f in file
    ]
