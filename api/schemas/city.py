from api.db import getDB
from api.schemas import StateResponse
from pydantic import (
    BaseModel,
    PositiveInt,
    constr,
    field_validator,
)
from api.models import State


def valid_state(id) -> bool:
    if id is None:
        return False
    db = getDB().__next__()
    return db.get(State, id) is not None


class CityRequest(BaseModel):
    name: constr(strip_whitespace=True, min_length=3, max_length=25)  # type: ignore
    state_id: PositiveInt | None = None

    @field_validator("name")
    @classmethod
    def vildate_name(cls, value: str):
        return value.title()

    @field_validator("state_id")
    @classmethod
    def vildate_state(cls, value: int):
        if not valid_state(value):
            raise ValueError(f"Invalid state ID {value}")

        return value


class CityResponse(CityRequest):
    id: int
    state: StateResponse

    class Config:
        from_attributes = True
