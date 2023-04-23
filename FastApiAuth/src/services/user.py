from functools import lru_cache
from typing import Union

import jwt
from pbkdf2 import crypt
from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .common import DBObjectService
from models.db_models import User
from db.db import get_db_session
from db.redis import get_redis
from utils.token import get_access_token
from core.config import app_settings


class UserService(DBObjectService):
    password_hash_iterations = 100

    async def create_user(self, login: str, password: str) -> Union[User, str]:
        hashed_password = crypt(
            password,
            iterations=self.password_hash_iterations
        )

        new_user = User(login=login, password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.commit()
        token_ = get_access_token(str(new_user.id))
        await self.cache.set(str(new_user.id), token_['access_token'], app_settings.token_ttl)
        return new_user, token_

    async def get_jwt(self, login: str, password: str) -> Union[User, str] | None:
        user = await self.db_session.execute(select(User).where(User.login == login))
        user = user.scalar()
        if user and user.password == crypt(password, user.password):
            token_ = get_access_token(str(user.id))
            await self.cache.set(str(user.id), token_['access_token'], app_settings.token_ttl)
            return user, token_

    async def check_token(self, token_: str) -> bool:
        payload = jwt.decode(
            token_,
            app_settings.secret_key,
            algorithms=['HS256'],
        )
        print(payload['id'])
        if (await self.cache.get(payload['id'])).decode() == token_:
            return True
        return False


@lru_cache
def get_user_service(
    db_session: AsyncSession = Depends(get_db_session),
    cache: Redis = Depends(get_redis),
) -> UserService:
    return UserService(db_session, cache)
