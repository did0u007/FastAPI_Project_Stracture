from api.core.helper import raise_error
from sqlalchemy.orm import Session
from api.models import File as UpFile
from fastapi import Depends, Response, UploadFile, File
from fastapi import status
from pathlib import Path
from typing import Dict
import datetime as dt
import shutil
import magic
from sqlalchemy.exc import IntegrityError
from api.core.helper import integrety_error_hundler as ieh


BASE_DIR = Path(__file__).parents[1]
PUBLIC_DIR = Path(BASE_DIR).joinpath("storage", "public")
PRIVATE_DIR = Path(BASE_DIR).joinpath("storage", "private")
print(dt.datetime.now(dt.UTC))


async def db_upload_file(
    db: Session,
    file: UploadFile = File(...),
    is_public=False,
) -> Dict[str, int | str]:  # type: ignore
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

        __file = UpFile()
        __file.file_name = file_name
        __file.path = str(Path(file_path).parent)

        db.add(__file)
        db.flush([__file])
        # db.commit()  # Here DB will be commited from the parent function who's call this one.
        return {
            "id": __file.id,
            "file_name": file_name,
        }

    except IntegrityError as e:
        db.rollback()
        raise_error(status.HTTP_409_CONFLICT, ieh(e.orig))


async def db_get_file(db: Session, filename: str, id: int = 0):
    db_file = db.query(UpFile).filter(File.file_name == filename).first()
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
