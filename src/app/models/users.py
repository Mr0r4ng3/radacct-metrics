from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.models.base import RecordModel


class User(RecordModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True)
    full_name: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool]
