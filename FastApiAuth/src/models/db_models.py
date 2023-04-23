import uuid

from sqlalchemy import Column, Text, String
from sqlalchemy.dialects.postgresql import UUID

from db.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    login = Column(String(length=255), unique=True)
    password = Column(Text, unique=False)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "User(id='%s', login='%s)" % (self.id, self.login)
