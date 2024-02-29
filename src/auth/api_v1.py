# TODO: Write a login endpoint with oauth2, hashing, auth bearer with JWT tokens
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/176b6fb1c9502bb516d27c166812b2ea706c8a8e/src/backend/app/app/api/api_v1/endpoints/login.py


from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import jwt, service
from src.auth.jwt import CurrentUser
from src.auth.schemas import AccessTokenResponse, AuthUserRequestForm, AuthUserResponse
from src.core.constants import ApiVersionPrefixes
from src.core.exceptions import BadRequest

auth_v1_router = APIRouter(
    prefix=ApiVersionPrefixes.AUTH_API_V1_PREFIX,
    tags=["Authentication Router (v1)"],
)


"""
Testing

email in db: example@mail.com
password in db: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW

SQL query:

insert into auth_user (email, password, is_admin) values (
'example@mail.com',
'$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
true
)

password to login in OpenAPI docs: secret
(uncomment AuthUserRequestForm b/c it won't pass the password check)
"""


@auth_v1_router.post("/login/access-token", response_model=AccessTokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> AccessTokenResponse:
    try:
        auth_data = AuthUserRequestForm(
            email=form_data.username, password=form_data.password
        )
    except ValueError as exc:
        raise BadRequest(detail=str(exc))

    user = await service.authenticate_user(auth_data)
    # TODO: add functionality to create refresh tokens
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user), token_type="bearer"
    )


@auth_v1_router.get("/users/me", response_model=AuthUserResponse)
async def read_user_me(current_user: CurrentUser) -> Any:
    return current_user
