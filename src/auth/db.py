from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    LargeBinary,
    MetaData,
    Select,
    String,
    Table,
    Update,
    func,
    insert,
    select,
)
from sqlalchemy.dialects.postgresql import UUID

from src.auth.schemas import AuthUserDB
from src.core.database import DB_NAMING_CONVENTION, async_engine

auth_metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

auth_user_table = Table(
    "auth_user",
    auth_metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

refresh_token_table = Table(
    "refresh_token",
    auth_metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("token", String, nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)


async def fetch_one(query: Select | Insert | Update) -> AuthUserDB | None:
    async with async_engine.begin() as conn:
        result = await conn.execute(query)

        first_row = result.first()
        return AuthUserDB(**first_row._asdict()) if first_row else None


async def find_one_by_id(user_id: int) -> AuthUserDB | None:
    if user_id is None:
        return None
    query = select(auth_user_table).where(auth_user_table.c.id == user_id)
    return await fetch_one(query)


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
