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
docker compose run --rm postgres-explorer python manage.py pg_explorer sample_app_person
```
```shell
docker compose exec -it postgres psql -U user db -c "SELECT * FROM heap_page_items(get_raw_page('sample_app_person', 0))"
```
