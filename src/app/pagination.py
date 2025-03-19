from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, func
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginationParams


def paginate(
    session: Session, statement: Select[Any], pagination: PaginationParams
) -> tuple[Sequence[Any], int]:
    page, limit = pagination
    offset = (page - 1) * limit

    paginated_statement = statement.offset(offset).limit(limit)
    results = session.execute(paginated_statement).all()

    count_statement = statement.with_only_columns(func.count()).order_by(None)
    total_count = session.execute(count_statement).scalar()

    if results and len(results[0]) == 1:
        results = [row[0] for row in results]
    else:
        results = list(results)

    return results, total_count
