from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"hello": "world"}


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ping")
async def ping() -> dict[str, bool]:
    return {"pong": True}


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


# Overriding pre-existing exception handlers
# NOTE: not sure if types are correct here.
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# Re-use FastAPI exception handlers (useful for logging or debugging)
# https://fastapi.tiangolo.com/tutorial/handling-errors/#re-use-fastapis-exception-handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler2(request: Request, exc: StarletteHTTPException):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
