from pydantic import BaseModel


class StateRequest(BaseModel):
    name: str


class StateResponse(StateRequest):
    id: int

    class Config:
        from_attributes = True
