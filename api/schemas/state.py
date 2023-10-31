from pydantic import BaseModel


class stateRequest(BaseModel):
    id: int
    name: str


class stateResponse(BaseModel):
    id: int
    name: str
