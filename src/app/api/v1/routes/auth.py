from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security.auth.func import authenticate, create_access_token
from app.core.security.auth.schemes import Token

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate(form_data.username, form_data.password)

    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
