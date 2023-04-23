start:
	while ! nc -z ${POSTGRES_HOST} ${DOCKER_DB_PORT}; do sleep 0.1; done
	while ! nc -z ${REDIS_HOST} ${REDIS_PORT}; do sleep 0.1; done
	python main.py