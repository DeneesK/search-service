import time
import datetime

import psycopg2
from redis import Redis
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as pg_conn

from utils.csv_extractor import extract_data_from_csv
from utils.store_to_posgres import PostgresStorage
from utils.postgres_extractor import PostgresExtractor
from utils.store_to_es import EsIndexCreator, EsStore
from core.config import etl_settings, logging
from db.redis import redis_conn
from db.es import elastic_conn


logger = logging.getLogger(__name__)


def main(pg_conn: pg_conn, cashe: Redis, es_conn: Elasticsearch):
    if cashe.get('etl_done_csv_postgres') != 1:
        logger.info('ETL started from *.csv to postgres')
        csv_extrac = extract_data_from_csv()
        pg_storage = PostgresStorage(conn=pg_conn)
        pg_storage.create_table()

        for row in csv_extrac:
            pg_storage.store_data(row.dict())
        cashe.set('etl_done_csv_postgres', 1)

    else:
        logger.info('ETL has already done task: from csv to postgres')

    pg_extractor = PostgresExtractor(pg_conn, cashe)

    if cashe.get('etl_index_created') != 1:
        logger.info(f'Create index: {etl_settings.index}')
        es_index_creator = EsIndexCreator(es_conn)
        es_index_creator.create_index(settings=etl_settings.es_settings, index=etl_settings.index)
        es_storage = EsStore(es_conn, etl_settings.index)
        cashe.set('etl_index_created', 1)

    es_storage.upload_data(pg_extractor.extract_data(itersize=etl_settings.itersize), itersize=etl_settings.itersize)
    cashe.set('last_date', str(datetime.datetime.now()))
    logger.info('ETL finished extracting and storing data')


if __name__ == '__main__':
    while True:
        with psycopg2.connect(dsn=etl_settings.sync_database_dsn,
                              cursor_factory=DictCursor) as pg_conn, redis_conn() as cashe, elastic_conn() as es_conn:
            main(pg_conn, cashe, es_conn)
        time.sleep(etl_settings.sleep_time)
