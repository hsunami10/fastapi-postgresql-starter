from sqlalchemy import Select, Table, select


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
