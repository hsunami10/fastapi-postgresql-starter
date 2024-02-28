import secrets
from typing import Any

from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import Environment


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    PROJECT_NAME: str
    ENVIRONMENT: Environment = Environment.PRODUCTION

    # TODO: change for prod
    SITE_DOMAIN: str = "https://myappdomain.com"
    SECURE_COOKIES: bool = True

    # Postgres Configuration
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",  # async driver
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # CORS Settings
    CORS_HEADERS: list[str] = []
    CORS_ORIGINS_REGEX: str | None = None
    CORS_ORIGINS: list[AnyHttpUrl] = []

    # TODO: change the field_validator, validator is deprecated in Pydantic v2
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 10 minutes: set it to something higher in the .env file for development
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)  # or openssl rand -hex 32
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

    SENTRY_DSN: HttpUrl | None = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str | None) -> str | None:
        if v is None or len(v) == 0:
            return None
        return v

    # FIRST_SUPERUSER: EmailStr
    # FIRST_SUPERUSER_PASSWORD: str
    # SMTP_TLS: bool = True
    # SMTP_PORT: int | None = None
    # SMTP_HOST: str | None = None
    # SMTP_USER: str | None = None
    # SMTP_PASSWORD: str | None = None
    # EMAILS_FROM_EMAIL: EmailStr | None = None
    # EMAILS_FROM_NAME: str | None = None

    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: str | None, values: dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v

    # USERS_OPEN_REGISTRATION: bool = False

    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    # EMAILS_ENABLED: bool = False

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )

    # EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    # # TODO: Implement refresh tokens
    # REFRESH_TOKEN_KEY: str = "refreshToken"
    # # https://fusionauth.io/articles/tokens/revoking-jwts
    # # https://www.loginradius.com/blog/identity/refresh-tokens-jwt-interaction/
    # REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 21  # 21 days


settings = Settings()
