import secrets

from pydantic import (
    AnyHttpUrl,
    HttpUrl,
    PostgresDsn,
    TypeAdapter,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import Environment, TestEnv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    PROJECT_NAME: str
    ENVIRONMENT: Environment = Environment.PRODUCTION
    TEST_ENV: TestEnv | None = None

    # TODO: change for prod
    SITE_DOMAIN: str = "https://myappdomain.com"
    SECURE_COOKIES: bool = True

    # Postgres Configuration
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URL", mode="before")
    def build_db_connection_str(
        cls, v: str | None, info: ValidationInfo
    ) -> PostgresDsn | None:
        if isinstance(v, str):
            return TypeAdapter(PostgresDsn).validate_strings(v)
        host = info.data["POSTGRES_HOST"]
        if (
            info.data["ENVIRONMENT"] == Environment.TESTING
            and info.data["TEST_ENV"] == TestEnv.LOCAL
        ):
            host = "localhost"
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",  # async driver
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=host,
            port=info.data["POSTGRES_PORT"],
            path=info.data["POSTGRES_DB"],
        )

    # CORS Settings
    CORS_HEADERS: list[str] = []
    CORS_ORIGINS_REGEX: str | None = None
    CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("CORS_ORIGINS", mode="before")
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

    # TODO: Implement refresh tokens
    REFRESH_TOKEN_COOKIE_KEY: str = "refreshToken"
    # https://auth0.com/docs/secure/tokens/refresh-tokens
    # https://fusionauth.io/articles/tokens/revoking-jwts
    # https://www.loginradius.com/blog/identity/refresh-tokens-jwt-interaction/
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 21  # 21 days

    SENTRY_DSN: HttpUrl | None = None

    @field_validator("SENTRY_DSN", mode="before")
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
    #         info.data["SMTP_HOST")
    #         and info.data["SMTP_PORT")
    #         and info.data["EMAILS_FROM_EMAIL")
    #     )

    # EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore


settings = Settings()
