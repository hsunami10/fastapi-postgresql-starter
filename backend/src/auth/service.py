import random
import string
from datetime import datetime, timedelta, timezone

from pydantic import UUID4

from src.auth import db, pwd_utils
from src.auth.exceptions import EmailTaken, InvalidCredentials
from src.auth.schemas import AuthUserDB, AuthUserRequestForm, RefreshTokenDB
from src.core.exceptions import NotFound
from src.db.models import refresh_token_table
from src.db.query import Query


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


async def get_refresh_token(refresh_token: str) -> RefreshTokenDB | None:
    select_query = refresh_token_table.select().where(
        refresh_token_table.c.token == refresh_token
    )

    return await db.find_refresh_token(select_query)


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    # datetime.fromordinal(1).replace(tzinfo=timezone.utc)
    update_query = (
        refresh_token_table.update()
        .values(expires_at=datetime.now(timezone.utc) - timedelta(days=1))
        .where(refresh_token_table.c.uuid == refresh_token_uuid)
    )

    await Query.execute(update_query)
