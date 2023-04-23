from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession


class DBObjectService:
    def __init__(self, db_session: AsyncSession, cahe: Redis) -> None:
        self.db_session = db_session
        self.cache = cahe
