import json
import logging

from pydantic import BaseSettings, PostgresDsn

from .logger import LOGGING


logging.basicConfig(**LOGGING)


class ETLSettings(BaseSettings):
    sync_database_dsn: PostgresDsn
    elastic_host: str
    redis_host: str
    redis_port: int
    index: str
    itersize: int
    sleep_time: float

    @property
    def es_settings(self) -> dict:
        with open('utils/es_settings.json', 'r') as file:
            return json.load(file)

    class Config:
        env_file = '.env'


etl_settings = ETLSettings()
