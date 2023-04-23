from elasticsearch import Elasticsearch, helpers

from core.config import logging, etl_settings


logger = logging.getLogger(__name__)


class EsIndexCreator:
    def __init__(self, es_object: Elasticsearch) -> None:
        self.es_object = es_object

    def create_index(self, settings: dict, index: str = etl_settings.index) -> None:
        if not self.es_object.indices.exists(index):
            try:
                self.es_object.indices.create(index=index, body=settings)
                logger.info('Index created')
            except Exception as ex:
                logger.error(ex)
        else:
            logger.info('Index already exists')


class EsStore:
    def __init__(self, es_conn: Elasticsearch, index: str) -> None:
        self.conn = es_conn
        self.index = index

    def upload_data(self, docs_generator, itersize: int = 100):
        try:
            lines, _ = helpers.bulk(
                client=self.conn,
                actions=docs_generator,
                index=self.index,
                chunk_size=itersize,
            )
        except Exception as ex:
            logger.error(ex)
