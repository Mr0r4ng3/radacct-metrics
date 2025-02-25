from fastapi import status
from fastapi.routing import APIRouter

from app.api.dependencies import SessionDep
from app.schemas.users import UserCreate, UserPublic
from app.services.users import UserService

router = APIRouter()


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(db: SessionDep, user: UserCreate):
    user_service = UserService(db)

    result = user_service.create(user)

    return result
