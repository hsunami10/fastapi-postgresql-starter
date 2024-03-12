import pytest
from fastapi import status
from httpx import AsyncClient

# from src.auth.constants import ErrorCode
from src.core.constants import ApiVersionPrefixes


@pytest.mark.asyncio
async def test_create_user_success(async_client: AsyncClient) -> None:
    path = "/"
    response = await async_client.post(
        ApiVersionPrefixes.AUTH_API_V1_PREFIX + path,
        data={
            "username": "email@fake.com",
            "password": "123Aa!",
        },
    )
    json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert json == {"id": 1}


# @pytest.mark.asyncio
# async def test_create_user_email_taken(
#     async_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
# ) -> None:
#     from src.auth.dependencies import service

#     async def fake_getter(*args, **kwargs):
#         return True

#     monkeypatch.setattr(service, "get_user_by_email", fake_getter)

#     resp = await async_client.post(
#         "/auth/users",
#         json={
#             "email": "email@fake.com",
#             "password": "123Aa!",
#         },
#     )
#     resp_json = resp.json()

#     assert resp.status_code == status.HTTP_400_BAD_REQUEST
#     assert resp_json["detail"] == ErrorCode.EMAIL_TAKEN
