from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: int
    file_name: str
