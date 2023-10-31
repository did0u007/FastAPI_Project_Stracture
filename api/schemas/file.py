from pydantic import BaseModel


class fileRequest(BaseModel):
    id: int
    url: str


class fileResponse(BaseModel):
    url: str
