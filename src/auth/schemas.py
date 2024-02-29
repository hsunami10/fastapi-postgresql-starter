import re
from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from src.core.schemas import CoreModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


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
            "digit or "
            "special symbol"
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
    password: str

    check_valid_password = field_validator("password", mode="after")(validate_password)

    is_admin: bool

    # TODO: figure out how to map sqlalchemy datetime to pydantic
    created_at: datetime
    updated_at: datetime | None = None


class JWTData(CoreModel):
    sub: str | None = None


class AccessTokenResponse(CoreModel):
    access_token: str
    token_type: str


class UserResponse(CoreModel):
    email: EmailStr
