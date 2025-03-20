from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import distinct, func, label, select
from sqlalchemy.orm import Session

from app.filters.radacct import RadacctFilter, RadacctTimeFilter
from app.models.radacct import Radacct
from app.pagination import paginate
from app.schemas.pagination import PaginationParams


class RadAcctService:
    def __init__(self, db: Session):
        self._db = db

    def list_all(
        self,
        table_name: str,
        pagination: PaginationParams,
        filters: RadacctFilter,
    ) -> tuple[Sequence[Radacct], int]:
        model = Radacct.get_model(table_name)

        filters.Constants.model = model

        statement = filters.filter(select(model))

        return paginate(session=self._db, statement=statement, pagination=pagination)

    def get_terminate_cause(
        self, table_name: str, filters: RadacctTimeFilter
    ) -> list[str]:
        model = Radacct.get_model(table_name)

        filters.Constants.model = model

        statement = filters.filter(select(distinct(model.acctterminatecause)))

        return self._db.scalars(statement).all()

    def get_sessions_metrics(
        self,
        table_name: str,
        filters: RadacctTimeFilter,
    ) -> list[tuple[datetime, int]]:
        model = Radacct.get_model(table_name)

        filters.Constants.model = model

        statement = filters.filter(
            select(
                label(
                    "interval_start",
                    func.date_format(model.acctstarttime, "%Y-%m-%d %H:%i:00"),
                ),
                label("session_count", func.count()),
            )
            .group_by(func.date_format(model.acctstarttime, "%Y-%m-%d %H:%i:00"))
            .order_by("interval_start")
        )

        results = self._db.execute(statement).all()

        return [(row.interval_start, row.session_count) for row in results]
