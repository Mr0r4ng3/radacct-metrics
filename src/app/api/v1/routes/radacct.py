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


@router.get(path="/", response_model=ListResourceResponse[RadacctSchema])
def get_all(
    tablename: str,
    pagination: PaginationParamsQuery,
    db: RadiusDbDep,
    filters: RadacctFilter = FilterDepends(RadacctFilter),  # noqa: B008
):
    if tablename not in get_tables():
        raise BadRequest("Invalid tablename")

    service = RadAcctService(db)

    results, count = service.list_all(
        table_name=tablename,
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
    tablename: str,
    db: RadiusDbDep,
    filters: RadacctTimeFilter = FilterDepends(RadacctTimeFilter),  # noqa: B008
):
    service = RadAcctService(db)

    return Response(data=service.get_terminate_cause(tablename, filters))


@router.get(path="/tables", response_model=Response[list[str]])
def get_available_tables():
    return Response(data=get_tables())
