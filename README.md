# Решение проектной работы 2 спринта

## Task 1

Добавлена [первая версия api](https://github.com/dimk00z/Admin_panel_sprint_2/tree/main/movies_admin/api/v1), в которой реализованы выгрузка json в формате [django_openapi.yml](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/files/django_openapi.yml).
Вся логика прописана в [views.py](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/movies_admin/api/v1/views.py).
Queryset собирается по фильмам с prefetch_related по "persons", "film_genres". Использована агрегация по жанрам и ролям персон.

## Task 2,3

Для деплоя проекта используется docker-compose.

Файл [docker-compose.yaml](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/docker-compose.yaml) содежит описание трех контейнеров проекта:

1. `postges_movie_db` - контейнер для развертывания postgres. В текущих настройках файлы базы данных связаны с путем `../postgres`

2. `movies_admin` - контейнер с бэкэндом джанги на основе [Dockerfile_django](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/Dockerfile_django). При развертывании в образ устанавливаются зависимости [production.txt](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/movies_admin/requirements/production.txt). Сервер работает через `gunicorn`.
3. `nginx` - контейнер с nginx вебсервером на основе [Dockerfile_nginx](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/nginx/Dockerfile_nginx) для отдачи статики и проброса с movies_admin:8000.

## Запуск проекта

1. Для корректной работы в movies_admin необходим `.env` файл на основе [.env_example](https://github.com/dimk00z/Admin_panel_sprint_2/blob/main/movies_admin/.env_example).
2. `docker-compose up -d --build` - для построения и запуска контейнеров.
Предполагается, что первичные миграции проведены и в базе есть данные администратора.
3. Пример ссылок:

http://localhost/admin/

http://localhost/api/v1/movies/

http://localhost/api/v1/movies/00af52ec-9345-4d66-adbe-50eb917f463a/

___


# Техническое задание

В качестве второго задания предлагаем расширить проект «Панель администратора»: запустить приложение через WSGI/ASGI, настроить отдачу статических файлов через Nginx и подготовить инфраструктуру для работы с Docker. Для этого перенесите в репозиторий код, который вы написали в первом спринте, и выполните задания из папки `tasks`.

## Используемые технологии

- Приложение запускается под управлением сервера WSGI/ASGI.
- Для отдачи [статических файлов](https://nginx.org/ru/docs/beginners_guide.html#static) используется **Nginx.**
- Виртуализация осуществляется в **Docker.**

## Основные компоненты системы

1. **Cервер WSGI/ASGI** — сервер с запущенным приложением.
2. **Nginx** — прокси-сервер, который является точкой входа для web-приложения.
3. **PostgreSQL** — реляционное хранилище данных. 
4. **ETL** — механизм обновления данных между PostgreSQL и ES.

## Схема сервиса

![all](images/all.png)

## Требования к проекту

1. Приложение должно быть запущено через WSGI/ASGI.
2. Все компоненты системы находятся в Docker.
3. Отдача статических файлов осуществляется за счёт Nginx.

## Рекомендации к проекту

1. Для работы с WSGI/ASGI-сервером база данных использует специального юзера.
2. Для взаимодействия между контейнерами используйте docker compose.


