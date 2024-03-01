from src.auth import db, pwd_utils
from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import AuthUserDB, AuthUserRequestForm
from src.core.exceptions import NotFound


async def get_user_by_id(user_id: int) -> AuthUserDB:
    user = await db.find_one_by_id(user_id)
    if not user:
        raise NotFound(detail="User not found")
    return user


async def authenticate_user(auth_data: AuthUserRequestForm) -> AuthUserDB:
    user = await db.find_one_by_email(auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not pwd_utils.check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user
