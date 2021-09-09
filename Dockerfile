FROM python:3.9.5-slim-buster

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p requirements

RUN pip install --upgrade pip

COPY movies_admin/requirements/*.txt requirements/

RUN pip install -r requirements/production.txt
RUN pip install -r requirements/dev.txt


COPY ./movies_admin .

# RUN python manage.py collectstatic --noinput

# CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
# ENTRYPOINT ["gunicorn", "config.wsgi", "--log-level", "debug", "--bind", "0.0.0.0:8000", "-w", "3"]
