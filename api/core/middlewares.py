from api.core.settings import IMG_TYPE
from api.core.helper import raise_error
from api.db.database import get_db
from sqlalchemy.orm import Session
from api.crud import file as fl
from api.core import Settings
from unittest import skip
from fastapi import Depends, File, Path, Query, Request, UploadFile
from typing import Annotated, List, Optional


async def query_limit(request: Request):
    max_args = int(Settings().STATE_QUERY_LIMIT) | 0  # type: ignore # 25
    query = request.query_params.multi_items()
    print(query)
    if len(query) > max_args:
        raise_error(422, "Too many query params")


async def query(
    skip: Annotated[int, Query(ge=0, allow_inf_nan=False)] = 0,  # type: ignore
    limit: Annotated[int, Query(ge=0, le=50)] = 50,
):
    return {"skip": skip, "limit": limit}


async def upload_file(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    muliples: bool = False,
):
    if not muliples:
        if (file := files[0]).content_type in IMG_TYPE:
            return await fl.db_upload_file(db, file)  # type: ignore

    return [
        await fl.db_upload_file(db, file)
        for file in files
        if file.content_type in IMG_TYPE
    ]
