from pydantic import BaseModel
from api.schemas import StateRequest, StateResponse


class City(BaseModel):
    id: int
    name: str


class CityRequest(City):
    state_id: int
    state: StateRequest


class CityResponse(City):
    state: StateResponse

    class Config:
        from_attributes = True
