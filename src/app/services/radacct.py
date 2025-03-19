from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.radacct import Radacct
from app.pagination import paginate
from app.schemas.pagination import PaginationParams

cached_classes = {}


class RadAcctService:
    def __init__(self, db: Session):
        self._db = db

    def _get_model(self, table_name: str) -> Radacct:
        class_name = f"Radacct_{table_name}"

        if table_name not in cached_classes:
            cached_classes[table_name] = type(
                class_name, (Radacct,), {"__tablename__": table_name}
            )

        return cached_classes[table_name]

    def list(
        self,
        table_name: str,
        pagination: PaginationParams,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> tuple[Sequence[Radacct], int]:
        model = self._get_model(table_name)
        statement = select(model)

        if start_time is not None:
            statement = statement.filter(model.acctstarttime >= start_time)

        if end_time is not None:
            statement = statement.filter(model.acctstoptime <= end_time)

        return paginate(session=self._db, statement=statement, pagination=pagination)
