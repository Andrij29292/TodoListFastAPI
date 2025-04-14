#!/bin/bash

DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="todosdb"
DB_USER="postgres"
DB_PASSWORD="1234"

RETRIES=10
WAIT_SECONDS=2

for i in $(seq 1 $RETRIES); do
  PGPASSWORD=$DB_PASSWORD pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    break
  else
    sleep $WAIT_SECONDS
  fi
done

if [ $i -eq $RETRIES ]; then
  exit 1
fi

exec uvicorn main:app --host 0.0.0.0 --port 8000
