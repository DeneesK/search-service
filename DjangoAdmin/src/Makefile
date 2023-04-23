start:
	while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do sleep 0.1; done
	python manage.py migrate
	python manage.py collectstatic --noinput
	python -m gunicorn --name admin -b 0.0.0.0:8000 conf.wsgi