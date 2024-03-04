from enum import Enum

from pydantic import BaseModel, ValidationInfo, field_validator


class TokenType(str, Enum):
    access = "Access Token"
    refresh = "Refresh Token"


class Token(BaseModel):
    token_type: str = "Bearer"
    token: str

    @field_validator("token")
    @classmethod
    def validate_token(cls, value, info: ValidationInfo):
        return f"{info.data.get('token_type')} {value}"


class TokenData(BaseModel):
    sub: str
    name: str | None = None
    host: str | None = None
    token_type: TokenType
