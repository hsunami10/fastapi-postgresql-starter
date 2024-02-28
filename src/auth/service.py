from sqlalchemy import select

from src.auth.exceptions import InvalidCredentials
from src.auth.models import auth_user_table
from src.auth.password_utils import check_password
from src.auth.schemas import AuthUserDB, AuthUserRequestForm
from src.database.engine import engine


async def get_user_by_id(user_id: str) -> AuthUserDB | None:
    query = select(auth_user_table).where(auth_user_table.c.id == user_id)

    # TODO: refactor connection into another file
    async with engine.begin() as conn:
        result = await conn.execute(query)

        first_row = result.first()
        return AuthUserDB(**first_row._asdict()) if first_row else None


async def get_user_by_email(email: str) -> AuthUserDB | None:
    query = select(auth_user_table).where(auth_user_table.c.email == email)

    # TODO: refactor connection into another file
    async with engine.begin() as conn:
        result = await conn.execute(query)

        first_row = result.first()
        return AuthUserDB(**first_row._asdict()) if first_row else None


async def authenticate_user(auth_data: AuthUserRequestForm) -> AuthUserDB:
    user = await get_user_by_email(auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user
