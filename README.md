# Postgres Explorer

Postgres raw data explorer using `pageinspect` extension.

## Create person table

```shell
docker compose exec -it db psql -U user db -c 'CREATE TABLE person (name VARCHAR(255), age INT)'
```

```shell
docker compose exec -it db psql -U user db -c '\d+ person'
```

## Insert rows

```shell
docker compose exec -it db psql -U user db -c "INSERT INTO person VALUES ('ivan', 34)"
```
```shell
docker compose exec -it db psql -U user db -c "INSERT INTO person VALUES ('alfonso', 15)"
```
```shell
docker compose exec -it db psql -U user db -c "SELECT * FROM person"
```

## Table pages inspector

Enable the pageinspect extension.
```shell
docker compose exec -it db psql -U user db -c "CREATE EXTENSION IF NOT EXISTS pageinspect"
```

```shell
docker compose exec -it db psql -U user db -c "SELECT relname, relpages FROM pg_class WHERE relname = 'person'"
```
```shell
docker compose exec -it db psql -U user db -c "SELECT * FROM heap_page_items(get_raw_page('person', 0))"
```
