import datetime as dt
import os
from pathlib import Path
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).parents[1]  # type: ignore
PUBLIC_DIR = Path(BASE_DIR).joinpath("storage", "public")
PRIVATE_DIR = Path(BASE_DIR).joinpath("storage", "private")

print(f"{round(dt.datetime.now().timestamp()):X}")


async def db_upload_file(db: Session, file: UploadFile, is_public=False):
    ROOT_DIR = PUBLIC_DIR if is_public else PRIVATE_DIR
    Y = dt.datetime.now(dt.UTC).year
    M = dt.datetime.now(dt.UTC).month
    DIR = Path(ROOT_DIR).joinpath(str(Y), str(M))
    FILE_NAME = f"{round(dt.datetime.now().timestamp()):X}_{file.filename}"
    FILE_PATH = Path(DIR).joinpath(FILE_NAME)
    Path(FILE_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(FILE_PATH, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)
