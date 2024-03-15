import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.db import auth_user_table
from src.auth.pwd_utils import check_password
from src.core.constants import ApiVersionPrefixes
from src.core.database import Query


@pytest.mark.asyncio
async def test_create_user_success(
    async_client: AsyncClient, async_connection: AsyncConnection
) -> None:
    email = "email@fake.com"
    plain_pwd = "123Aa!"
    response = await async_client.post(
        f"{ApiVersionPrefixes.AUTH_API_V1_PREFIX}/",
        data={
            "username": email,
            "password": plain_pwd,
        },
    )

    result = await async_connection.execute(Query.select_by_id(auth_user_table, 1))
    assert result.rowcount == 1
    first_row = result.first()
    assert first_row is not None

    db = first_row._asdict()
    assert db["id"] == 1
    assert db["email"] == email
    assert check_password(plain_pwd, db["password"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1}


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
