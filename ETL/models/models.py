from datetime import datetime

from pydantic import BaseModel, validator


class PostModelShort(BaseModel):
    id: str | None
    text: str


class PostModelFull(PostModelShort):
    created_date: datetime
    rubrics: list

    @validator('rubrics', pre=True)
    def convert_rubrics(cls, value) -> list:
        if isinstance(value, list):
            return value
        lst = value[1:-1].split(', ')
        result = [elem[1:-1] for elem in lst]
        return result

    @validator('created_date', pre=True)
    def conver_date(cls, value):
        if isinstance(value, datetime):
            return value
        value = value.replace('-', '.')[:17]
        try:
            datetime_obj = datetime.strptime(value, '%d.%m.%Y %H:%M')
        except Exception:
            datetime_obj = datetime.strptime(value, '%Y.%m.%d %H:%M')
        return datetime_obj
