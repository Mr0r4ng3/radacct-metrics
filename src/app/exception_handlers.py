from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import RadacctMetricsException, RadacctMetricsRequestValidationError


def custom_exception_handler(
    request: Request,  # noqa: ARG001
    exc: RadacctMetricsException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers,
    )


def custom_request_validation_exception_handler(
    request: Request,  # noqa: ARG001
    exc: RequestValidationError | RadacctMetricsRequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": type(exc).__name__, "detail": jsonable_encoder(exc.errors())},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(RadacctMetricsException, custom_exception_handler)
    app.add_exception_handler(
        RequestValidationError, custom_request_validation_exception_handler
    )
    app.add_exception_handler(
        RadacctMetricsRequestValidationError,
        custom_request_validation_exception_handler,
    )
