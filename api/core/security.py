import datetime as dt
from typing import Annotated

from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.core import Settings
from api.db.database import get_db
from api.models import User, RefreshToken
from api.schemas.token import Token, TokenData, TokenType

pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")
outh2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_pass(password: str) -> str:
    return pwd_contex.hash(password)


def verify_pass(plaintext: str, hash_pass: str) -> bool:
    return pwd_contex.verify(plaintext, hash_pass)


def get_bearer_token(bearer: str):
    b = bearer.replace("Bearer", "", 1)
    return b.strip()


async def authenticate_user(data, db: Session) -> User:
    username = data.username
    password = data.password

    db_user: User | None = db.query(User).filter(User.username == username).first()

    if not db_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials!, User Not Exist.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_pass(password, db_user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials!, Password don't match.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_user


async def create_refresh_token(
    request: Request,
    data: TokenData,
    expire_delta: dt.timedelta | None = None,
):
    payload = data.model_dump()
    host = request.client.host  # type: ignore
    now = dt.datetime.now(dt.UTC)
    if expire_delta:
        expire = now + expire_delta
    else:
        expire = now + dt.timedelta(
            days=int(Settings.REFRESH_TOKEN_EXPIRE_DAYS)  # type: ignore
        )
    payload.update({"exp": expire, "host": host, "token_type": TokenType.refresh})
    print(payload)
    encoded_jwt = jwt.encode(payload, Settings.JWT_SECRET_KEY, Settings.JWT_ALGORITHM)  # type: ignore

    return encoded_jwt


async def create_access_token(
    data: TokenData,
    expire_delta: dt.timedelta | None = None,
):
    payload = data.model_dump()
    now = dt.datetime.now(dt.UTC)
    if expire_delta:
        expire = now + expire_delta
    else:
        expire = now + dt.timedelta(
            minutes=int(Settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # type: ignore
        )
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, Settings.JWT_SECRET_KEY, Settings.JWT_ALGORITHM)  # type: ignore

    return f"Bearer {encoded_jwt}"


async def get_current_user(
    token: Annotated[str, Depends(outh2_schema)],
    db: Annotated[Session, Depends(get_db)],
):
    print(get_bearer_token(token))
    token = get_bearer_token(token)

    try:
        token_data = jwt.decode(token, Settings.JWT_SECRET_KEY, [Settings.JWT_ALGORITHM])  # type: ignore
        username = token_data.get("sub", None)

        if not username:
            raise JWTError

        user = db.query(User).filter(User.username == username).first()
        return user

    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired.")
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token.")


async def refresh_access_token(request: Request, access_token, refresh_token):
    old_token = access_token
    refresh_token = refresh_token
    # check if sub is the same in bothe tokens

    try:

        access_token_data = jwt.get_unverified_claims(access_token)
        refresh_token_data = jwt.decode(
            refresh_token, Settings.JWT_SECRET_KEY, [Settings.JWT_ALGORITHM]  # type: ignore
        )
        if request.client.host != refresh_token_data.get("host", None):  # type: ignore
            raise JWSError
        if access_token_data.get("sub", "access") != refresh_token_data.get(
            "sub", "refresh"
        ):
            raise JWSError
        new_data = access_token_data
        return await create_access_token(TokenData(**new_data))

    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired.")
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token.")


async def create_tokens(request: Request, data: TokenData) -> Response:
    """
    return a response with access token on header['Authorization']
    and refresh token on HTTP_ONLY Cookies
    """
    access_token: str = request.headers.get("Authorization", "Not Authorized")
    refresh_token: str = request.cookies.get("refresh_token", "Not Authorized")
    if access_token == "Not Authorized":
        access_token = await create_access_token(data, expire_delta=None)
        refresh_token = await create_refresh_token(request, data, None)

    else:
        try:
            jwt.decode(access_token, Settings.JWT_SECRET_KEY, [Settings.JWT_ALGORITHM])  # type: ignore
        except ExpiredSignatureError:

            if refresh_token == "Not Authorized":
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token.")
            access_token = await refresh_access_token(
                request, access_token, refresh_token
            )
        except JWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token.")

    resp = Response()
    resp.headers["Authorization"] = access_token
    resp.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=Settings.COOKIE_EXPIRE_DAYS,  # type: ignore
        httponly=True,
    )

    return resp
