from sqlalchemy import (
    Insert,
    Select,
    Update,
    insert,
    select,
)

from src.auth.schemas import AuthUserDB
from src.db.engine import async_engine
from src.db.models import auth_user_table
from src.db.query import Query


# TODO: Refactor with generic Pydantic types
async def fetch_one(query: Select | Insert | Update) -> AuthUserDB | None:
    async with async_engine.begin() as conn:
        result = await conn.execute(query)

        first_row = result.first()
        return AuthUserDB(**first_row._asdict()) if first_row else None


async def find_one_by_id(user_id: int) -> AuthUserDB | None:
    if user_id is None:
        return None
    return await fetch_one(Query.select_by_id(auth_user_table, user_id))


async def find_one_by_email(email: str) -> AuthUserDB | None:
    if email is None:
        return None
    query = select(auth_user_table).where(auth_user_table.c.email == email)
    return await fetch_one(query)


async def create_with_email_pwd(email: str, password: bytes) -> AuthUserDB | None:
    if email is None or password is None:
        return None
    query = (
        insert(auth_user_table)
        .values(email=email, password=password)
        .returning(auth_user_table)
    )
    return await fetch_one(query)
