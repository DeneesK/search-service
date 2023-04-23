import uuid

from pydantic import BaseModel


class UserData(BaseModel):
    login: str
    password: str


class User(BaseModel):
    login: str
    id: uuid.UUID
    access_token: str = ''


class Token(BaseModel):
    access_token: str
