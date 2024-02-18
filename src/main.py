from fastapi import FastAPI
# from src.tutorial.router import router as tutorial_router

from src.tutorial import (
    path_params_router,
    query_params_router,
    request_body_router,
    validations_router,
    cookie_header_router,
    response_pydantic_router,
    status_codes_router,
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
