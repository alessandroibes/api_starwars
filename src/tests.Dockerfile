# pull official base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY dependencies/requirements.txt /app/requirements.txt
COPY dependencies/requirements-dev.txt /app/requirements-dev.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements-dev.txt

COPY starwars/ /app/starwars
COPY pytest.ini /app/pytest.ini
COPY wsgi.ini /app/wsgi.ini
COPY tests/ /app/tests

CMD ["pytest"]