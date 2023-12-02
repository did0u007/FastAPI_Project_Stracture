from pydantic import BaseModel, PositiveInt, constr


class StateRequest(BaseModel):
    name: constr(strip_whitespace=True, to_upper=True, min_length=3, max_length=25)  # type: ignore


class StateResponse(StateRequest):
    id: PositiveInt

    class Config:
        from_attributes = True
