from pydantic import BaseModel
from api.core.enums import userType
from api.schemas import fileResponse
from api.schemas.city import cityResponse
from api.schemas.state import stateResponse


class userRequest(BaseModel):
    id: int
    name: str
    username: str
    email: str
    password: str
    profile_img: fileResponse
    user_type: userType
    city_id: int | None
    state_id: int
    address: str
    phone: str


class userResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    profile_img: str | None
    remember_token: str | None
    user_type: userType
    city: cityResponse | None
    state: stateResponse
    address: str
    phone: str
