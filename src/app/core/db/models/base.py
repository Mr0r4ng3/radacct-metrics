from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.timezone import utc_now


class Model(DeclarativeBase):
    __abstract__ = True


class TimestampedModel(Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=utc_now, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=utc_now,
        nullable=True,
        default=None,
        index=True,
    )

    deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, default=None, index=True
    )

    def set_deleted_at(self) -> None:
        self.deleted_at = utc_now()


class RecordModel(TimestampedModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, self.__class__) and self.id == __value.id
