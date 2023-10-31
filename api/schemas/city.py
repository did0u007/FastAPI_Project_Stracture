from pydantic import BaseModel
from api.schemas import stateRequest, stateResponse


class cityRequest(BaseModel):
    id: int
    name: str
    state_id: int
    state: stateRequest


class cityResponse(BaseModel):
    id: int
    name: str
    state: stateResponse
