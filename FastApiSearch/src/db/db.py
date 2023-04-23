from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base


Base = declarative_base()


async_session: AsyncSession | None = None


async def get_db_session() -> Generator:
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session
