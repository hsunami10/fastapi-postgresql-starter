# TODO: Write a login endpoint with oauth2, hashing, auth bearer with JWT tokens
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/176b6fb1c9502bb516d27c166812b2ea706c8a8e/src/backend/app/app/api/api_v1/endpoints/login.py


from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import jwt, service, utils
from src.auth.schemas import AccessTokenResponse, AuthUserRequestForm, AuthUserResponse
from src.core.constants import ApiVersionPrefixes

auth_v1_router = APIRouter(
    prefix=ApiVersionPrefixes.AUTH_API_V1_PREFIX,
    tags=["Authentication Router (v1)"],
)


"""
Testing

TODO: Remove this docstring
Use this generator to test: https://bcrypt-generator.com/
"""


@auth_v1_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AuthUserResponse
)
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:
    auth_data = AuthUserRequestForm(
        email=form_data.username, password=form_data.password
    )
    # TODO: add functionality for email verification
    return await service.create_user(auth_data)


@auth_v1_router.post("/login", response_model=AccessTokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> Any:
    auth_data = AuthUserRequestForm(
        email=form_data.username, password=form_data.password
    )

    user = await service.authenticate_user(auth_data)
    refresh_token = await service.create_refresh_token(user_id=user.id)

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user),
        refresh_token=refresh_token,
        token_type="bearer",
    )
