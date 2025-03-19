from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=Any)


class Response(BaseModel, Generic[T]):
    data: T
    metadata: dict[str, Any] = {}
