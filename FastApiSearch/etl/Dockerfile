FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app/"

COPY . .

RUN pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt