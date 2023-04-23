import redis
from redis import Redis

from core.config import etl_settings, logging


logger = logging.getLogger(__name__)


def redis_conn() -> Redis:
    try:
        conn = redis.from_url(f'redis://{etl_settings.redis_host}:{etl_settings.redis_port}')
    except Exception as ex:
        logger.error(ex)
    return conn
