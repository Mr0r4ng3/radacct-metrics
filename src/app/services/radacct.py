from datetime import datetime

from sqlalchemy.orm import Session

from app.models.radacct import Radacct

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

    def get_all(
        self,
        table_name: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Radacct]:
        model = self._get_model(table_name)
        query = self._db.query(model)

        if start_time is not None:
            query = query.filter(model.acctstarttime >= start_time)

        if end_time is not None:
            query = query.filter(model.acctstoptime <= end_time)

        return query.offset(offset).limit(limit).all()
