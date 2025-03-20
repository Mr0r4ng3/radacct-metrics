from datetime import datetime
from typing import Annotated

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends

from app.core.db.dependencies import RadiusDbDep
from app.core.db.radius_db import get_tables
from app.depends.pagination import PaginationParamsQuery
from app.exceptions import BadRequest
from app.filters.radacct import RadacctFilter, RadacctTimeFilter
from app.schemas.radacct import RadacctSchema
from app.schemas.responses import ListResourceResponse, Response
from app.services.radacct import RadAcctService

router = APIRouter()


def get_table_name(
    table_name=Query(  # noqa: B008
        alias="tablename",
        title="Table name",
        description="Radacct table name used for data retrieval.",
        min_length=1,
        max_length=100,
        regex="^radacct[0-9]*$",
    ),
) -> str:
    if table_name not in get_tables():
        raise BadRequest("Invalid tablename")

    return table_name


TableNameQuery = Annotated[str, Depends(get_table_name)]


@router.get(path="/", response_model=ListResourceResponse[RadacctSchema])
def get_all(
    table_name: TableNameQuery,
    pagination: PaginationParamsQuery,
    db: RadiusDbDep,
    filters: RadacctFilter = FilterDepends(RadacctFilter),  # noqa: B008
):
    service = RadAcctService(db)

    results, count = service.list_all(
        table_name=table_name,
        filters=filters,
        pagination=pagination,
    )

    return ListResourceResponse.from_paginated_results(
        [RadacctSchema.model_validate(result) for result in results],
        count,
        pagination,
    )


@router.get(path="/terminate-causes", response_model=Response[list[str]])
def get_terminate_causes(
    table_name: TableNameQuery,
    db: RadiusDbDep,
    filters: RadacctTimeFilter = FilterDepends(RadacctTimeFilter),  # noqa: B008
):
    service = RadAcctService(db)

    return Response(data=service.get_terminate_cause(table_name, filters))


@router.get(path="/tables", response_model=Response[list[str]])
def get_available_tables():
    return Response(data=get_tables())


@router.get(
    path="/metrics/sessions", response_model=Response[list[tuple[datetime, int]]]
)
def get_sessions_metrics(
    table_name: TableNameQuery,
    db: RadiusDbDep,
    filters: RadacctTimeFilter = FilterDepends(RadacctTimeFilter),  # noqa: B008
) -> Response[list[tuple[datetime, int]]]:
    service = RadAcctService(db)

    return Response(data=service.get_sessions_metrics(table_name, filters))
