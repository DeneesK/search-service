from psycopg2.extensions import connection as pg_conn

from core.config import logging


logger = logging.getLogger(__name__)


class PostgresStorage:
    def __init__(self, conn: pg_conn) -> None:
        self.conn = conn

    def create_table(self):
        curs = self.conn.cursor()
        try:
            curs.execute(
                """
                CREATE EXTENSION IF NOT EXISTS pgcrypto;
                CREATE TABLE IF NOT EXISTS posts
                (id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                text TEXT,
                created_date timestamp,
                rubrics TEXT[]);
                """,
            )
        except Exception as ex:
            logger.error(ex)

    def store_data(self, post: dict):
        curs = self.conn.cursor()
        try:
            curs.execute("INSERT INTO posts VALUES (gen_random_uuid(), %(text)s, %(created_date)s, %(rubrics)s);",
                         post)
        except Exception as ex:
            logger.error(ex)
