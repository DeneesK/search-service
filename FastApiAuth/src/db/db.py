from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()

async_session: AsyncSession | None = None


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
