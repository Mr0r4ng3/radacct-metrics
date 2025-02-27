from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.db.database import SessionLocal
from app.core.security.auth.schemes import TokenData
from app.schemas.users import UserPublic
from app.services.users import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def authenticate(username: str, plain_password: str):
    with SessionLocal() as db:
        service = UserService(db=db)

        user = service.authenticate(username, plain_password)

        if user is None:
            raise InvalidCredentialsException

        return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise InvalidCredentialsException

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise InvalidCredentialsException  # noqa: B904

    with SessionLocal() as db:
        service = UserService(db=db)

        user = service.get_user_by_username(username=token_data.username)

        if user is None:
            raise InvalidCredentialsException

        return user


def get_current_active_user(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active"
        )

    return current_user
