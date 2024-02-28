# TODO: Write a login endpoint with oauth2, hashing, auth bearer with JWT tokens
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/176b6fb1c9502bb516d27c166812b2ea706c8a8e/src/backend/app/app/api/api_v1/endpoints/login.py


from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.jwt import create_access_token
from src.auth.schemas import AccessTokenResponse, AuthUserRequestForm
from src.auth.service import authenticate_user
from src.core.constants import ApiVersionPrefixes

router = APIRouter(prefix=f"{ApiVersionPrefixes.API_V1_PREFIX}/auth")


@router.post("/login/access-token", response_model=AccessTokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> AccessTokenResponse:
    auth_data = AuthUserRequestForm(
        email=form_data.username, password=form_data.password
    )
    user = await authenticate_user(auth_data)
    access_token = create_access_token(user)
    # TODO: add functionality to create refresh tokens too
    return AccessTokenResponse(access_token=access_token, token_type="bearer")
