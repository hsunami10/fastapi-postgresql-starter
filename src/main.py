from fastapi import FastAPI
from src.tutorial.router import router as tutorial_router

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

app.include_router(tutorial_router, prefix="/tutorial", tags=["tutorial"])
