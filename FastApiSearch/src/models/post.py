import uuid
import datetime

from sqlalchemy import Column, DateTime, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from db.db import Base


class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, unique=False, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    rubrics = Column(ARRAY(item_type=Text), nullable=False, unique=False)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "Post(id='%s', text='%s)" % (self.id, self.text)
