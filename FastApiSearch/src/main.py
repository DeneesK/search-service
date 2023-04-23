import uvicorn
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from db import db
from db import es
from api.v1.search import router
from core.config import app_settings


app = FastAPI(
    title='Text Search',
    description='The service get text query and searches it for the text of the document in the index',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)


@app.on_event('startup')
async def startup():
    es.es = AsyncElasticsearch(hosts=[app_settings.elastic_host])
    engine = create_async_engine(
        app_settings.database_dsn,
        future=True,
        echo=True
    )
    db.async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@app.on_event('shutdown')
async def shutdown():
    await db.es.close()
    await db.async_session.close()


app.include_router(router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
