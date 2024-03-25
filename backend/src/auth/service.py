import random
import string
import uuid
from datetime import datetime, timedelta, timezone

from pydantic import UUID4

from src.auth import db, pwd_utils
from src.auth.exceptions import EmailTaken, InvalidCredentials
from src.auth.schemas import AuthUserDB, AuthUserRequestForm, RefreshTokenDB
from src.core.config import settings
from src.core.exceptions import NotFound
from src.db import query_helper
from src.db.models import auth_user_table, refresh_token_table


async def get_user_by_id(user_id: int) -> AuthUserDB:
    db_user = await query_helper.fetch_one(
        query_helper.select_by_id(auth_user_table, user_id)
    )
    if not db_user:
        raise NotFound(detail="User not found")
    return AuthUserDB(**db_user)


async def create_user(auth_data: AuthUserRequestForm) -> AuthUserDB:
    db_user = await db.create_with_email_pwd(
        auth_data.email, pwd_utils.hash_password(auth_data.password)
    )
    if not db_user:
        raise EmailTaken()

    return AuthUserDB(**db_user)


async def authenticate_user(auth_data: AuthUserRequestForm) -> AuthUserDB:
    db_user = await query_helper.fetch_one(
        query_helper.select_account_by_email(auth_data.email)
    )
    if not db_user:
        raise InvalidCredentials()

    user = AuthUserDB(**db_user)
    if not pwd_utils.check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user


async def create_refresh_token(user_id: int, refresh_token: str | None = None) -> str:
    if not refresh_token:
        refresh_token = "".join(
            random.choices(population=string.ascii_letters + string.digits, k=20)
        )

    expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    insert_query = refresh_token_table.insert().values(
        uuid=uuid.uuid4(),
        token=refresh_token,
        expires_at=datetime.now(timezone.utc) + expires_delta,
        user_id=user_id,
    )
    await query_helper.execute(insert_query)

    return refresh_token


async def get_refresh_token(refresh_token: str) -> RefreshTokenDB | None:
    query = refresh_token_table.select().where(
        refresh_token_table.c.token == refresh_token
    )
    db_refresh_token = await query_helper.fetch_one(query)
    return RefreshTokenDB(**db_refresh_token) if db_refresh_token is not None else None


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    # datetime.fromordinal(1).replace(tzinfo=timezone.utc)
    update_query = (
        refresh_token_table.update()
        .values(expires_at=datetime.now(timezone.utc) - timedelta(days=1))
        .where(refresh_token_table.c.uuid == refresh_token_uuid)
    )

    await query_helper.execute(update_query)
