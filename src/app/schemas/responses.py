from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel):
    message: str
    code: int


class Response(ResponseBase):
    result: T | None


class ResponseError(ResponseBase):
    pass
