from typing import NamedTuple

from app.schemas.base import Schema


class PaginationParams(NamedTuple):
    page: int
    limit: int


class Pagination(Schema):
    total_count: int
    max_page: int
