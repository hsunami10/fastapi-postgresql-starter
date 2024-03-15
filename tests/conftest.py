import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from src.core.config import settings
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def run_migrations() -> Generator[None, None, None]:
    print("running migrations..")
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")


# NOTE: Deprecated and doesn't work for some reason
# https://github.com/pytest-dev/pytest-asyncio/blob/b22d84e1f0d53920352be4c66d1b6c7f7a9ce005/pytest_asyncio/plugin.py#L692C1-L703C2
# https://github.com/pytest-dev/pytest-asyncio/discussions/587
# @pytest.fixture(scope="session")
# def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

# TODO: FIX
# @pytest_asyncio.fixture(scope="session")
# async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
#     engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))
#     yield engine
#     await engine.dispose()


# @pytest_asyncio.fixture(scope="function")
# async def async_connection(
#     async_engine: AsyncEngine,
# ) -> AsyncGenerator[AsyncConnection, None]:
#     async with async_engine.begin() as connection:
#         yield connection


# NOTE: Works, but is there any way to re-create the engine with scope=session?
@pytest_asyncio.fixture(scope="function")
async def async_connection() -> AsyncGenerator[AsyncConnection, None]:
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))

    async with engine.begin() as connection:
        yield connection
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    host, port = os.getenv("SITE_DOMAIN"), "8080"
    transport = ASGITransport(app=app)  # type: ignore[arg-type]

    async with AsyncClient(
        transport=transport, base_url=f"http://{host}:{port}"
    ) as client:
        yield client
