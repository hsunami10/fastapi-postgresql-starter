import os

import debugpy
from fastapi import FastAPI, Request, status
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from src.account.api_v1 import account_v1_router
from src.auth.api_v1 import auth_v1_router
from src.core.config import settings
from src.core.constants import Environment, TestEnv
from src.tutorial import (
    cookie_header_router,
    dependencies_router,
    error_handling_router,
    path_params_router,
    query_params_router,
    request_body_router,
    response_pydantic_router,
    status_codes_router,
    validations_router,
)

if (
    os.getenv("ENVIRONMENT") == Environment.TESTING
    and os.getenv("TEST_ENV") == TestEnv.DOCKER
):
    debugpy.listen(("0.0.0.0", 5555))
    print("Waiting for VSCode to attach...")
    debugpy.wait_for_client()

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),  # ["*"]
    allow_headers=settings.CORS_HEADERS,  # ["*"]
)


@app.get("/", include_in_schema=False, status_code=status.HTTP_200_OK)
async def root() -> dict[str, str]:
    return {"hello": "world"}


@app.get("/healthcheck", include_in_schema=False, status_code=status.HTTP_200_OK)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


# TODO: Fine-tune custom exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    print(f"Logging HTTP error: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(ValidationError)
async def validation_error_exception_handler(request: Request, exc: ValidationError):
    print(f"Logging ValidationError: {repr(exc)}")
    return await request_validation_exception_handler(request, exc)


app.include_router(auth_v1_router)
app.include_router(account_v1_router)

app.include_router(path_params_router)
app.include_router(query_params_router)
app.include_router(request_body_router)
app.include_router(validations_router)
app.include_router(cookie_header_router)
app.include_router(response_pydantic_router)
app.include_router(status_codes_router)
app.include_router(error_handling_router)
app.include_router(dependencies_router)


"""
Error Handling
https://fastapi.tiangolo.com/tutorial/handling-errors/
"""


# Custom error handlers
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
