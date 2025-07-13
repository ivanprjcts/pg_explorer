# Postgres Explorer

Postgres raw data explorer using `pageinspect` extension.

## Create person table

```shell
docker compose run --rm postgres-explorer python manage.py migrate
```

## Insert rows

```shell
docker compose run --rm postgres-explorer python manage.py add_person
```
```shell
docker compose run --rm postgres-explorer python manage.py list_people
```

## Table pages inspector

Enable the pageinspect extension.
```shell
docker compose exec -it postgres psql -U user db -c "CREATE EXTENSION IF NOT EXISTS pageinspect"
```

```shell
docker compose run --rm postgres-explorer python manage.py explore sample_app_person
```

## Unit tests

Run unit tests using `pytest`.
```shell
docker compose run --rm postgres-explorer pytest
```
