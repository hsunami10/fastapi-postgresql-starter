import random
import string

from src.auth import db, pwd_utils
from src.auth.exceptions import EmailTaken, InvalidCredentials
from src.auth.schemas import AuthUserDB, AuthUserRequestForm
from src.core.exceptions import NotFound


async def get_user_by_id(user_id: int) -> AuthUserDB:
    user = await db.find_one_by_id(user_id)
    if not user:
        raise NotFound(detail="User not found")
    return user


async def create_user(auth_data: AuthUserRequestForm) -> AuthUserDB:
    # if await db.find_one_by_email(auth_data.email):
    #     raise EmailTaken()
    user = await db.create_with_email_pwd(
        auth_data.email, pwd_utils.hash_password(auth_data.password)
    )
    if not user:
        raise EmailTaken()

    return user


async def authenticate_user(auth_data: AuthUserRequestForm) -> AuthUserDB:
    user = await db.find_one_by_email(auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not pwd_utils.check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user


async def create_refresh_token(user_id: int, refresh_token: str | None = None) -> str:
    if not refresh_token:
        refresh_token = "".join(
            random.choices(population=string.ascii_letters + string.digits, k=20)
        )

    await db.insert_refresh_token(user_id, refresh_token)
    return refresh_token
