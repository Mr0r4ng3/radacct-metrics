from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep
from app.core.security.auth.func import authenticate, create_access_token
from app.core.security.auth.schemes import Token
from app.exceptions import InvalidCredentials
from app.schemas.responses import Response

router = APIRouter()


@router.post(
    "/token",
    response_model=Response[Token],
    responses={401: {"description": "Invalid credentials"}},
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
) -> Token:
    user = authenticate(form_data.username, form_data.password, db=db)

    if not user:
        raise InvalidCredentials()

    access_token = create_access_token(data={"sub": user.username})

    return Response(data=Token(access_token=access_token, token_type="bearer"))
