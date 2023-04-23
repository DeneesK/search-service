start:
	while ! nc -z ${POSTGRES_HOST} ${DOCKER_DB_PORT}; do sleep 0.1; done
	python manage.py migrate
	python -m gunicorn --name admin -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000 conf.wsgi