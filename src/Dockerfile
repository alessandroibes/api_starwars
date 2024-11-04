# pull official base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY dependencies/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN pip install uwsgi

COPY starwars/ /app/starwars
COPY wsgi.py /app/wsgi.py
COPY wsgi.ini /app/wsgi.ini

EXPOSE 5000

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]