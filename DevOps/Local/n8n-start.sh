#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ai-agents-with-langchain"
POSTGRES_COMPOSE="${SCRIPT_DIR}/Postgres/docker-compose.yaml"
N8N_DIR="${SCRIPT_DIR}/n8n"
N8N_COMPOSE="${N8N_DIR}/docker-compose.yaml"
N8N_ENV="${N8N_DIR}/.env"

if [[ ! -f "${N8N_ENV}" ]]; then
  if [[ -f "${N8N_DIR}/.env.example" ]]; then
    ENCRYPTION_KEY="$(openssl rand -hex 24)"
    sed "s/replace-with-a-stable-32-plus-char-secret/${ENCRYPTION_KEY}/" \
      "${N8N_DIR}/.env.example" > "${N8N_ENV}"
    echo "Created ${N8N_ENV} with a new N8N_ENCRYPTION_KEY."
    echo "Keep this file safe — changing the key breaks saved credentials."
  else
    echo "Missing ${N8N_ENV}. Create it from .env.example first." >&2
    exit 1
  fi
fi

echo "Ensuring Postgres is running..."
docker compose -p "${PROJECT_NAME}" -f "${POSTGRES_COMPOSE}" up -d

echo "Waiting for Postgres to be ready..."
for _ in $(seq 1 30); do
  if docker exec ai-agents-with-langchain-postgres pg_isready -U postgres -d app >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "Ensuring n8n database exists..."
docker exec ai-agents-with-langchain-postgres \
  psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'n8n'" \
  | grep -q 1 \
  || docker exec ai-agents-with-langchain-postgres \
       psql -U postgres -c "CREATE DATABASE n8n;"

echo "Starting n8n..."
docker compose -p "${PROJECT_NAME}" -f "${N8N_COMPOSE}" up -d

echo "n8n started: http://localhost:5678"
