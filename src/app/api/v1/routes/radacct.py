from datetime import datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from app.core.db.radacct_db import get_db, get_metadata
from app.exceptions import BadRequest
from app.schemas.radacct import RadacctSchema
from app.schemas.responses import Response
from app.services.radacct import RadAcctService

router = APIRouter()


def get_tables():
    metadata = get_metadata()

    return [table for table in metadata.tables if table.startswith("radacct")]


@router.get(path="/", response_model=Response[list[RadacctSchema]])
def get_all(
    tablename: str,
    start_time: str | None = None,
    end_time: str | None = None,
    page: int = 1,
    limit: int = 100,
):
    if tablename not in get_tables():
        raise BadRequest("Invalid tablename")

    offset = (page - 1) * limit

    if start_time is not None:
        start_time = datetime.fromisoformat(start_time)

    if end_time is not None:
        end_time = datetime.fromisoformat(end_time)

    with get_db() as db:
        service = RadAcctService(db)

        return Response(
            data=service.get_all(tablename, start_time, end_time, limit, offset)
        )


@router.get(path="/tables", response_model=Response[list[str]])
def get_available_tables():
    return Response(data=get_tables())
