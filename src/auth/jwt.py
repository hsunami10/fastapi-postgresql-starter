from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.exceptions import AuthRequired, InvalidCredentials, InvalidToken
from src.auth.schemas import AuthUserDB, JWTData
from src.auth.service import get_user_by_id
from src.core.config import settings
from src.core.constants import ApiVersionPrefixes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{ApiVersionPrefixes.API_V1_PREFIX}/login/access-token"
)


def create_access_token(
    user: AuthUserDB,
    expires_delta: timedelta = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    ),
) -> str:
    jwt_data = {
        "sub": str(user.id),
        "exp": datetime.now(timezone.utc) + expires_delta,
        "is_admin": bool(user.is_admin),
    }
    encoded_jwt = jwt.encode(
        jwt_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


TokenDep = Annotated[str, Depends(oauth2_scheme)]


def parse_jwt_from_token(token: TokenDep) -> JWTData:
    if not token:
        raise AuthRequired()

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def get_current_user(token: TokenDep) -> AuthUserDB:
    """
    Validate token and get current user.
    """
    try:
        payload = parse_jwt_from_token(token)
        user_id = payload.sub
        if user_id is None:
            raise InvalidCredentials()
    except JWTError:
        raise InvalidCredentials()

    user = await get_user_by_id(user_id)
    if user is None:
        raise InvalidCredentials()
    return user
