from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.users import User
from app.schemas.users import UserCreate, UserPublic


class UserService:
    def __init__(self, db: Session):
        self._db = db

    def create(self, user_in: UserCreate) -> UserPublic:
        user = User(
            username=user_in.username,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
            is_active=True,
        )

        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        return UserPublic(
            id=user.id,
            full_name=user.full_name,
            username=user.username,
            is_active=user.is_active,
        )
