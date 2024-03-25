from typing import Any

from sqlalchemy import Insert, Select, Table, Update, select

from src.db.engine import async_engine


class Query:
    """
    A custom class with static methods of commonly used SQLAlchemy queries.
    """

    @staticmethod
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

    @staticmethod
    async def execute(query: Insert | Update) -> None:
        async with async_engine.begin() as conn:
            await conn.execute(query)

    @staticmethod
    async def fetch_one(query: Select | Insert | Update) -> dict[str, Any] | None:
        async with async_engine.begin() as conn:
            result = await conn.execute(query)

            first_row = result.first()
            return first_row._asdict() if first_row else None
