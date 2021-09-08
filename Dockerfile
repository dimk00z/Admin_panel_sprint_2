FROM python:3.9.5-slim-buster

WORKDIR /code

RUN mkdir -p requirements

COPY movies_admin/requirements/*.txt requirements/

RUN pip install -r requirements/production.txt

COPY ./movies_admin .

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
