from src.core.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class ErrorDetail:
    AUTHENTICATION_REQUIRED = "Authentication required."
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorDetail.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorDetail.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorDetail.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorDetail.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = ErrorDetail.EMAIL_TAKEN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorDetail.REFRESH_TOKEN_NOT_VALID
