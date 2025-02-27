from fastapi import status
from fastapi.routing import APIRouter

from app.api.dependencies import SessionDep
from app.core.security.auth.dependencies import UserDep
from app.schemas.users import UserCreate, UserPublic
from app.services.users import UserService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(current_user: UserDep, db: SessionDep, user: UserCreate) -> UserPublic:  # noqa: ARG001
    user_service = UserService(db)

    result = user_service.create(user)

    return result


@router.get("/me")
def read_user_me(current_user: UserDep):
    return current_user
