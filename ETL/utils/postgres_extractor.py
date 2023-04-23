from typing import Generator

from psycopg2.extensions import connection as pg_conn
from redis import Redis

from models.models import PostModelShort
from core.config import logging


logger = logging.getLogger(__name__)


class PostgresExtractor:
    def __init__(self, conn: pg_conn, cashe: Redis, model: PostModelShort = PostModelShort) -> None:
        self.conn = conn
        self.model = model
        self.last_date = cashe.get('last_date').decode() if cashe.get('last_date') else '2000-01-01'

    def extract_data(self, itersize: int = 100) -> Generator:
        curs = self.conn.cursor()
        curs.itersize = itersize
        try:
            curs.execute(
                f"""SELECT id, text, created_date, rubrics
                FROM posts
                WHERE DATE(created_date) >= DATE('{self.last_date}')"""
            )
        except Exception as ex:
            logger.error(ex)

        for data in curs:
            try:
                yield self.model.parse_obj(data).dict()
            except Exception as ex:
                logger.error(ex)
