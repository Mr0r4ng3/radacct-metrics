from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.api.dependencies import SessionDep
from app.core.config import settings
from app.core.security.auth.schemes import TokenData
from app.exceptions import InvalidCredentials, NotAuthenticated, Unauthorized
from app.schemas.users import UserPublic
from app.services.users import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")


def authenticate(username: str, plain_password: str, db: Session):
    service = UserService(db=db)

    user = service.authenticate(username, plain_password)

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise InvalidCredentials()

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise NotAuthenticated()  # noqa: B904

    service = UserService(db=db)

    user = service.get_user_by_username(username=token_data.username)

    if user is None:
        raise InvalidCredentials()

    return user


def get_current_active_user(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
):
    if current_user.disabled:
        raise Unauthorized()

    return current_user
