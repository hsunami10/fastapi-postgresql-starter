from sqlalchemy import Select, Table, select
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings

async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


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
