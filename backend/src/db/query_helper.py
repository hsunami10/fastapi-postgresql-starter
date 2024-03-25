from typing import Any

from sqlalchemy import Insert, Select, Table, Update, select

from src.db.engine import async_engine
from src.db.models import auth_user_table


def select_by_id(table: Table, id: int) -> Select:
    """Selects rows from a table with a specified id.

    SELECT FROM [table] WHERE [table].id == [id];

    Args:
        table (Table): The SQLAlchemy table to query from.
        id (int): The id to find.

    Returns:
        Select: An object used to construct SQLAlchemy select statements.
    """
    return select(table).where(table.c.id == id)


def select_account_by_email(email: str):
    return select(auth_user_table).where(auth_user_table.c.email == email)


async def execute(query: Insert | Update) -> None:
    async with async_engine.begin() as conn:
        await conn.execute(query)


async def fetch_one(query: Select | Insert | Update) -> dict[str, Any] | None:
    async with async_engine.begin() as conn:
        result = await conn.execute(query)

        first_row = result.first()
        return first_row._asdict() if first_row else None
