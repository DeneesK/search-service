from pydantic import BaseModel


class SearchSchema(BaseModel):
    query: str

    @property
    def search_query(self):
        return {'query':
                {'query_string':
                    {'query': self.query}},
                'size': 10, 'from': 0, 'sort': []}
