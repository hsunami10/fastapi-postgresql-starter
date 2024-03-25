from datetime import datetime, timezone
from typing import Annotated

from fastapi import Cookie, Depends

from src.auth import service
from src.auth.exceptions import RefreshTokenNotValid
from src.auth.schemas import AuthUserDB, RefreshTokenDB
from src.core.config import settings


async def valid_refresh_token(
    refresh_token: Annotated[str, Cookie(alias=settings.REFRESH_TOKEN_KEY)],
) -> RefreshTokenDB:
    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: Annotated[RefreshTokenDB, Depends(valid_refresh_token)],
) -> AuthUserDB:
    user = await service.get_user_by_id(refresh_token.user_id)
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: RefreshTokenDB) -> bool:
    return datetime.now(timezone.utc) <= db_refresh_token.expires_at
