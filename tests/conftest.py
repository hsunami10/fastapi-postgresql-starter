import os
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection

from src.db.engine import async_engine
from src.db.models import base_metadata
from src.main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def run_migrations() -> AsyncGenerator[None, None]:
    async with async_engine.connect() as connection:
        await connection.run_sync(base_metadata.drop_all)
        await connection.run_sync(base_metadata.create_all)
        await connection.commit()
        yield
        await connection.run_sync(base_metadata.drop_all)
        await connection.commit()


# NOTE: Deprecated and doesn't work for some reason
# https://github.com/pytest-dev/pytest-asyncio/blob/b22d84e1f0d53920352be4c66d1b6c7f7a9ce005/pytest_asyncio/plugin.py#L692C1-L703C2
# https://github.com/pytest-dev/pytest-asyncio/discussions/587
# @pytest.fixture(scope="session")
# def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as connection:
        yield connection


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    host, port = os.getenv("SITE_DOMAIN"), "8080"
    transport = ASGITransport(app=app)  # type: ignore[arg-type]

    async with AsyncClient(
        transport=transport, base_url=f"http://{host}:{port}"
    ) as client:
        yield client
