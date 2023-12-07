from typing import List
from fastapi import File, UploadFile
from pydantic import BaseModel


class UploadFileRequest(BaseModel):
    files: List[UploadFile] = File(...)


class UploadFileResponse(BaseModel):
    id: int
    file_name: str
