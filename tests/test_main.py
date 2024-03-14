import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(async_client: AsyncClient) -> None:
    response = await async_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"hello": "world"}


@pytest.mark.asyncio
async def test_healthcheck(async_client: AsyncClient) -> None:
    response = await async_client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
