from api.core.helper import raise_error
from api.db import getDB
from sqlalchemy.orm import Session
from api.models import File
from fastapi import Depends, Response, UploadFile
from fastapi import status
from pathlib import Path
from typing import List
import datetime as dt
import shutil
import magic

from api.schemas.upload import UploadFileResponse


BASE_DIR = Path(__file__).parents[1]
PUBLIC_DIR = Path(BASE_DIR).joinpath("storage", "public")
PRIVATE_DIR = Path(BASE_DIR).joinpath("storage", "private")
print(dt.datetime.now(dt.UTC))


async def db_upload_file(
    file: UploadFile,
    db: Session,
    is_public=False,
):
    root_dir = PUBLIC_DIR if is_public else PRIVATE_DIR
    __tmp = dt.datetime.now(dt.UTC)
    y_dir = str(__tmp.year)
    m_dir = str(__tmp.month)
    file_name = (
        f"{round(__tmp.timestamp()):X}.{file.filename.split('.')[-1]}"  # type:ignore
    )
    file_path = Path(root_dir).joinpath(y_dir, m_dir, file_name)
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w+b") as buffer:
            shutil.copyfileobj(file.file, buffer)

        __file = File()
        __file.file_name = file_name
        __file.path = str(Path(file_path).parent)

        db.add(__file)
        db.flush([__file])
        db.commit()
        return {
            "id": __file.id,
            "file_name": file_name,
        }

    except Exception as e:
        raise_error(status.HTTP_504_GATEWAY_TIMEOUT, str(e))


async def db_get_file(db: Session, filename: str, id: int = 0):
    db_file = db.query(File).filter(File.file_name == filename).first()
    if db_file is None:
        raise_error(status.HTTP_404_NOT_FOUND, f"File not found {filename}")
    file = Path(db_file.path).joinpath(db_file.file_name)  # type: ignore
    data = b""
    print(file)
    with open(file, "rb") as f:
        data += f.read()
    resp = Response(data, media_type=magic.from_buffer(data))
    resp.headers["Content-Disposition"] = f"inline; filename={db_file.file_name}"  # type: ignore

    return resp
