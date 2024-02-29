from typing import Any

from fastapi import HTTPException, status


class CoreHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Internal server error"

    def __init__(
        self, detail: str | dict[str, Any] | None = None, **kwargs: dict[str, Any]
    ) -> None:
        # If detail is not passed in manually, default to the DETAIL class property
        d = self.DETAIL if detail is None else detail
        super().__init__(status_code=self.STATUS_CODE, detail=d, **kwargs)


class PermissionDenied(CoreHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(CoreHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Resource not found"


class BadRequest(CoreHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(CoreHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})
