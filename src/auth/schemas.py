from pydantic import ConfigDict, EmailStr

from src.core.schemas import CoreModel


# Shared properties
class AuthUserBase(CoreModel):
    email: EmailStr | None = None
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class AuthUserCreate(AuthUserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class AuthUserUpdate(AuthUserBase):
    password: str | None = None


class AuthUserInDBBase(AuthUserBase):
    # https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class AuthUser(AuthUserInDBBase):
    pass


class AuthUserInDBCore(CoreModel):
    id: int
    email: EmailStr
    is_admin: bool

    # TODO: figure out how to map sqlalchemy datetime to pydantic
    # created_at: datetime
    # updated_at: datetime | None = None


# Additional properties stored in DB
class AuthUserInDBPassword(AuthUserInDBBase):
    password: str


class AccessTokenResponse(CoreModel):
    access_token: str
    token_type: str


class JWTData(CoreModel):
    sub: str | None = None
    is_admin: bool = False


class TokenPayload(CoreModel):
    sub: int | None = None
