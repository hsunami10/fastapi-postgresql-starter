# TODO: Write a login endpoint with oauth2, hashing, auth bearer with JWT tokens
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/176b6fb1c9502bb516d27c166812b2ea706c8a8e/src/backend/app/app/api/api_v1/endpoints/login.py


from typing import Any

from fastapi import APIRouter

from src.auth.jwt import CurrentUser
from src.auth.schemas import AuthUserResponse
from src.core.constants import ApiVersionPrefixes

account_v1_router = APIRouter(
    prefix=ApiVersionPrefixes.ACCOUNTS_API_V1_PREFIX,
    tags=["Accounts Router (v1)"],
)


@account_v1_router.get("/me", response_model=AuthUserResponse)
async def read_user_me(current_user: CurrentUser) -> Any:
    return current_user
