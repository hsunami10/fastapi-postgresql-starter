import secrets

from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    # 10 minutes: set it to something higher in the .env file for development
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)  # or openssl rand -hex 32
    JWT_ALGORITHM: str = "HS256"

    # TODO: Implement refresh tokens
    REFRESH_TOKEN_KEY: str = "refreshToken"
    # https://fusionauth.io/articles/tokens/revoking-jwts
    # https://www.loginradius.com/blog/identity/refresh-tokens-jwt-interaction/
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True


auth_settings = AuthSettings()
