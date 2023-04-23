import uuid

from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    id: uuid.UUID | str
    text: str
    created_date: datetime
    rubrics: list
