from typing import Optional
from api.schemas import StateResponse
from pydantic import BaseModel


class CityRequest(BaseModel):
    name: str
    state_id: Optional[int]


class CityResponse(CityRequest):
    id: int
    state: StateResponse

    class Config:
        from_attributes = True
