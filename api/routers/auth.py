from typing import Annotated

from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.core.security import authenticate_user, create_tokens, get_current_user
from api.db import getDB
from api.schemas import Token, TokenType, TokenData
from api.schemas.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_access_token(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(getDB),
):
    user = await authenticate_user(form_data, db)
    token_data = TokenData(
        sub=user.username,
        name=user.name,
        token_type=TokenType.access,
    )
    return await create_tokens(request, token_data)  # type: ignore


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def get_authenticated_user(user: Annotated[User, Depends(get_current_user)]):
    return user
