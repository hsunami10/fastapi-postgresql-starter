from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from src.auth.config import auth_settings
from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/login/access-token"
)


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta = timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ),
) -> str:
    jwt_data = {"sub": str(subject), "exp": datetime.now(timezone.utc) + expires_delta}
    encoded_jwt = jwt.encode(
        jwt_data, auth_settings.SECRET_KEY, algorithm=auth_settings.JWT_ALGORITHM
    )
    return encoded_jwt
