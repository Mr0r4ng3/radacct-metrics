from typing import Any, Literal, LiteralString, NotRequired, TypedDict

from fastapi import status
from pydantic import BaseModel, Field, create_model
from pydantic_core import ErrorDetails, InitErrorDetails, PydanticCustomError
from pydantic_core import ValidationError as PydanticValidationError


class RadacctMetricsException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers

    @classmethod
    def schema(cls) -> type[BaseModel]:
        error_literal = Literal[cls.__name__]  # type: ignore

        return create_model(
            cls.__name__,
            error=(error_literal, Field(examples=[cls.__name__])),
            detail=(str, ...),
        )


class InvalidCredentials(RadacctMetricsException):
    def __init__(
        self,
        message: str = "Invalid credentials",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)


class Unauthorized(RadacctMetricsException):
    def __init__(
        self,
        message: str = "Unauthorized",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)


class NotAuthenticated(RadacctMetricsException):
    def __init__(
        self,
        message: str = "Not authenticated",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)


class BadRequest(RadacctMetricsException):
    def __init__(
        self,
        message: str = "Bad request",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, status_code)


class ValidationError(TypedDict):
    loc: tuple[int | str, ...]
    msg: LiteralString
    type: LiteralString
    input: Any
    ctx: NotRequired[dict[str, Any]]


class RadacctMetricsRequestValidationError(RadacctMetricsException):
    def __init__(self, errors: list[ValidationError]) -> None:
        self._errors = errors

    def errors(self) -> list[ErrorDetails]:
        pydantic_errors: list[InitErrorDetails] = []

        for error in self._errors:
            pydantic_errors.append(
                {
                    "type": PydanticCustomError(error["type"], error["msg"]),
                    "loc": error["loc"],
                    "input": error["input"],
                }
            )

        pydantic_error = PydanticValidationError.from_exception_data(
            self.__class__.__name__, pydantic_errors
        )

        return pydantic_error.errors()
