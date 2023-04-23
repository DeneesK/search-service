start:
	while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do sleep 0.1; done
	while ! nc -z ${REDIS_HOST} ${REDIS_PORT}; do sleep 0.1; done
	while ! nc -z ${ELASTIC_HOST} ${ES_PORT}; do sleep 0.1; done
	python -m gunicorn --name search -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000 main:app