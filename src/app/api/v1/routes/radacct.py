from datetime import datetime

from fastapi.routing import APIRouter

from app.core.db.radacct_db import get_db, get_metadata
from app.depends.pagination import PaginationParamsQuery
from app.exceptions import BadRequest
from app.schemas.radacct import RadacctSchema
from app.schemas.responses import ListResourceResponse, Response
from app.services.radacct import RadAcctService

router = APIRouter()


def get_tables():
    metadata = get_metadata()

    return [table for table in metadata.tables if table.startswith("radacct")]


@router.get(path="/", response_model=ListResourceResponse[RadacctSchema])
def get_all(
    tablename: str,
    pagination: PaginationParamsQuery,
    start_time: str | None = None,
    end_time: str | None = None,
):
    if tablename not in get_tables():
        raise BadRequest("Invalid tablename")

    if start_time is not None:
        start_time = datetime.fromisoformat(start_time)

    if end_time is not None:
        end_time = datetime.fromisoformat(end_time)

    with get_db() as db:
        service = RadAcctService(db)

        results, count = service.list(
            table_name=tablename,
            pagination=pagination,
            start_time=start_time,
            end_time=end_time,
        )

        return ListResourceResponse.from_paginated_results(
            [RadacctSchema.model_validate(result) for result in results],
            count,
            pagination,
        )


@router.get(path="/tables", response_model=Response[list[str]])
def get_available_tables():
    return Response(data=get_tables())
