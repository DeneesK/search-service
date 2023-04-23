from elasticsearch import Elasticsearch

from core.config import etl_settings, logging


logger = logging.getLogger(__name__)


def elastic_conn():
    try:
        return Elasticsearch([etl_settings.elastic_host])
    except Exception as ex:
        logger.error(ex)
