#!/bin/bash

echo "Stopping and removing existing containers and volumes..."
docker compose down -v

echo "Rebuilding containers without cache..."
docker compose build --no-cache

echo "Starting containers in detached mode..."
docker compose up -d

echo "Waiting for database to be ready..."
sleep 5

# Detect the container name dynamically (case-insensitive match for 'db').
DB_CONTAINER=$(docker ps --filter "name=db" --format "{{.Names}}" | head -n 1)

if [ -z "$DB_CONTAINER" ]; then
  echo "Could not find the DB container."
  exit 1
fi

echo "Connecting to PostgreSQL inside container: $DB_CONTAINER"
docker exec -it "$DB_CONTAINER" psql -U postgres -d bytebox
