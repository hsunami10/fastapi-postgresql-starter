import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

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


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    host, port = os.getenv("SITE_DOMAIN"), "8080"
    transport = ASGITransport(app=app)  # type: ignore[arg-type]

    async with AsyncClient(
        transport=transport, base_url=f"http://{host}:{port}"
    ) as client:
        yield client
