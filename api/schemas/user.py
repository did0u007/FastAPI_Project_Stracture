import re
from typing import Any
from pydantic import (
    BaseModel,
    EmailStr,
    PositiveInt,
    ValidationInfo,
    constr,
    field_validator,
)
from api.core.enums import UserType
from api.schemas import CityResponse, StateResponse

password_pattern = re.compile(
    r"^(?=.*[a-z])"  # At least one lowercase letter
    r"(?=.*[A-Z])"  # At least one uppercase letter
    r'(?=.*[!@#$%^&*()_+{}|":<>?`~])'  # At least one special character
    r"(?=\S+$)"  # No spaces allowed
    r".{8,}$"  # Minimum 8 characters
)


class User(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=25)  # type: ignore
    name: str | None
    address: str | None
    email: EmailStr
    phone: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if " " in value:
            raise ValueError("Username can't have whitespace characters")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value, info: ValidationInfo):
        if value is None:
            return (info.username).capitalize()  # type: ignore
        return value


class UserRequest(User):
    password: str  # type: ignore
    confirmed_password: str
    state_id: PositiveInt
    city_id: PositiveInt | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not password_pattern.match(value):
            raise ValueError(
                "Password must be Min 08 characters have at least one character upper/lower and at least one special character, without whitespaces."
            )
        return value

    @field_validator("confirmed_password")
    @classmethod
    def validate_confirmed_password(cls, value, info: ValidationInfo):
        if value != info.password:  # type: ignore
            raise ValueError("Confirmed password must be identical to the password")


class UserResponse(User):
    id: int
    profile_img: str | None
    # remember_token: str | None
    city: CityResponse | None
    state: StateResponse
    user_type: UserType

    class Config:
        from_attributes = True
