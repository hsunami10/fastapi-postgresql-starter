from fastapi import Response

from src.auth.schemas import CookieModel
from src.core.config import settings


def set_response_cookie(response: Response, cookie: CookieModel) -> None:
    response.set_cookie(
        key=cookie.key,
        value=cookie.value,
        max_age=cookie.max_age,
        domain=cookie.domain,
        secure=cookie.secure,
        httponly=cookie.httponly,
        samesite=cookie.samesite,
    )


def get_refresh_token_cookie(
    refresh_token: str,
    is_expired: bool = False,
) -> CookieModel:
    base_cookie = CookieModel(
        key=settings.REFRESH_TOKEN_COOKIE_KEY,
        httponly=True,
        samesite="none"
        if settings.SECURE_COOKIES
        else "lax",  # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#none
        secure=settings.SECURE_COOKIES,
        domain=settings.SITE_DOMAIN,
    )
    if is_expired:
        return base_cookie

    base_cookie.value = refresh_token
    base_cookie.max_age = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    return base_cookie
