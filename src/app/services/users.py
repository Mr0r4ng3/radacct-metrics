from fastapi import HTTPException
from sqlalchemy import select
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

    def get_user_by_username(self, username: str) -> UserPublic | None:
        stmt = select(User).where(User.username == username)

        user = self._db.scalars(stmt).first()

        if user is None:
            return None

        return UserPublic(
            id=user.id,
            full_name=user.full_name,
            username=user.username,
            is_active=user.is_active,
        )

    def authenticate(self, username: str, plain_password: str) -> UserPublic | None:
        stmt = select(User).where(User.username == username)

        user: User = self._db.scalars(stmt).first()

        if user is None:
            return None

        if verify_password(
            plain_password=plain_password, hashed_password=user.hashed_password
        ):
            return UserPublic(
                id=user.id,
                full_name=user.full_name,
                username=user.username,
                is_active=user.is_active,
            )
