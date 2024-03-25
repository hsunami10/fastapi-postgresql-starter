from typing import Any

from sqlalchemy import insert

from src.auth.exceptions import EmailTaken
from src.db import query_helper
from src.db.engine import async_engine
from src.db.models import auth_user_table


async def create_with_email_pwd(email: str, password: bytes) -> dict[str, Any] | None:
    if email is None or password is None:
        return None

    select_query = query_helper.select_account_by_email(email)
    insert_query = (
        insert(auth_user_table)
        .values(email=email, password=password)
        .returning(auth_user_table)
    )

    # TODO: Connection is closed error when:
    #   - wiping + migrating database and refreshing browser
    #   - only on the very first query
    async with async_engine.begin() as conn:
        select_result = await conn.execute(select_query)
        if select_result.first() is not None:
            raise EmailTaken()

        result = await conn.execute(insert_query)
        first_row = result.first()
        return first_row._asdict() if first_row else None
