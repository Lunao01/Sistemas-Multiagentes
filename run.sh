#!/usr/bin/env bash

f () {
    touch src/.env
    echo DB_USER=postgres >> src/.env
    echo DB_PASSWORD=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 30) >> src/.env
}

[ -f src/.env ] || f

t="$(pwd)"

cd src
docker compose up --build
cd "$t"