import re
from datetime import datetime
from typing import Literal

from pydantic import UUID4, EmailStr, Field, field_validator

from src.core.schemas import CoreModel

# https://uibakery.io/regex-library/password-regex-python
STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,128}$"
)


def validate_password(password: str) -> str:
    """Validate the password with regex.

    DO NOT IMPORT!

    Args:
        password (str): The value of the field "password"
    """
    if not re.match(STRONG_PASSWORD_PATTERN, password):
        raise ValueError(
            "Password must contain at least "
            "one lower character, "
            "one upper character, "
            "one digit, "
            "one special symbol"
        )

    return password


class AuthUserRequestForm(CoreModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

    check_valid_password = field_validator("password", mode="after")(validate_password)


class AuthUserDB(CoreModel):
    """
    Pydantic model for SQLAlchemy auth_user table.
    """

    id: int
    email: EmailStr
    password: bytes
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None = None


class AuthUserResponse(CoreModel):
    id: int


class RefreshTokenDB(CoreModel):
    """
    Pydantic model for SQLAlchemy refresh_token table.
    """

    uuid: UUID4
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime | None = None


class CookieModel(CoreModel):
    key: str
    httponly: bool
    samesite: Literal["lax", "strict", "none"] | None
    secure: bool
    domain: str
    value: str = ""
    max_age: int | None = None


class JWTData(CoreModel):
    sub: str | None = None


class AccessTokenResponse(CoreModel):
    access_token: str
    refresh_token: str
    token_type: str
