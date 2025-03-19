from fastapi import status
from fastapi.routing import APIRouter

from app.api.dependencies import SessionDep
from app.core.security.auth.dependencies import UserDep
from app.schemas.responses import Response
from app.schemas.users import UserCreate, UserPublic
from app.services.users import UserService

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=Response[UserPublic]
)
def create_user(
    current_user: UserDep,  # noqa: ARG001
    db: SessionDep,
    user: UserCreate,
) -> Response[UserPublic]:
    user_service = UserService(db)

    result = user_service.create(user)

    return Response(data=result)


@router.get("/me", response_model=Response[UserPublic])
def read_user_me(current_user: UserDep):
    return Response(data=current_user)
