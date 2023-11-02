from pydantic import BaseModel


class FileResponse(BaseModel):
    url: str

    class Config:
        from_attributes = True


class FileRequest(FileResponse):
    id: int
