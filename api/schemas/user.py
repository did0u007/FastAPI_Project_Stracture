from pydantic import BaseModel
from api.core.enums import UserType
from api.schemas import FileResponse
from api.schemas.city import CityResponse
from api.schemas.state import StateResponse


class User(BaseModel):
    name: str
    username: str
    email: str
    address: str
    phone: str


class UserRequest(User):
    password: str
    state_id: int
    city_id: int | None


class UserResponse(User):
    id: int
    profile_img: str | None
    remember_token: str | None
    city: CityResponse | None
    state: StateResponse
    user_type: UserType

    class Config:
        from_attributes = True
