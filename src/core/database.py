from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
