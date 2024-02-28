from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select

from src.auth.exceptions import AuthRequired, InvalidCredentials, InvalidToken
from src.auth.schemas import AuthUserInDBCore, JWTData
from src.core.config import settings
from src.database import auth_user_table, engine

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/login/access-token"
)


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    ),
) -> str:
    jwt_data = {"sub": str(subject), "exp": datetime.now(timezone.utc) + expires_delta}
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


# TODO: return pydantic user model
async def get_user_from_db(user_id: str) -> AuthUserInDBCore | None:
    query = select(auth_user_table).where(auth_user_table.c.id == user_id)
    async with engine.begin() as conn:
        result = await conn.execute(query)

        if result.rowcount > 0:
            first_row = result.first()
            return AuthUserInDBCore(**first_row._asdict()) if first_row else None
        return None


async def get_current_user(token: TokenDep) -> AuthUserInDBCore:
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

    user = await get_user_from_db(user_id)
    if user is None:
        raise InvalidCredentials()
    return user
