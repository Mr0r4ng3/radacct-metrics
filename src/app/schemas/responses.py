import math
from collections.abc import Sequence
from typing import Any, Generic, Self, TypedDict, TypeVar

from app.schemas.base import Schema
from app.schemas.pagination import Pagination, PaginationParams

T = TypeVar("T", bound=Any)
S = TypeVar("S", bound=Schema)


class Response(Schema, Generic[T]):
    data: T
    metadata: dict[str, Any] = {}


class ListResourceMetadata(TypedDict):
    pagination: Pagination


class ListResourceResponse(Schema, Generic[S]):
    data: list[S]
    metadata: ListResourceMetadata

    @classmethod
    def from_paginated_results(
        cls, items: Sequence[S], total_count: int, pagination_params: PaginationParams
    ) -> Self:
        return cls(
            data=list(items),
            metadata={
                "pagination": Pagination(
                    total_count=total_count,
                    max_page=math.ceil(total_count / pagination_params.limit),
                ),
            },
        )
