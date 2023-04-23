import csv

from models.models import PostModelFull
from core.config import logging


logger = logging.getLogger(__name__)


def extract_data_from_csv() -> PostModelFull:
    with open('utils/posts.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            try:
                yield PostModelFull.parse_obj(row)
            except Exception as ex:
                logger.error(ex)
