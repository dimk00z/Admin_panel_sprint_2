FROM python:3.9.5-slim-buster

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p requirements
RUN pip install --upgrade pip
COPY movies_admin/requirements/*.txt requirements/
RUN pip install -r requirements/production.txt

COPY ./movies_admin .

RUN python manage.py collectstatic --noinput