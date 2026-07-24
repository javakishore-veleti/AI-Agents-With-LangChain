#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ai-agents-with-langchain"
POSTGRES_COMPOSE="${SCRIPT_DIR}/Postgres/docker-compose.yaml"
N8N_DIR="${SCRIPT_DIR}/n8n"
N8N_COMPOSE="${N8N_DIR}/docker-compose.yaml"
N8N_ENV="${N8N_DIR}/.env"
N8N_URL="http://localhost:5678"

ensure_env_file() {
  if [[ -f "${N8N_ENV}" ]]; then
    return
  fi
  if [[ ! -f "${N8N_DIR}/.env.example" ]]; then
    echo "Missing ${N8N_ENV}. Create it from .env.example first." >&2
    exit 1
  fi
  ENCRYPTION_KEY="$(openssl rand -hex 24)"
  sed "s/replace-with-a-stable-32-plus-char-secret/${ENCRYPTION_KEY}/" \
    "${N8N_DIR}/.env.example" > "${N8N_ENV}"
  echo "Created ${N8N_ENV} with a new N8N_ENCRYPTION_KEY."
  echo "Keep this file safe — changing the key breaks saved credentials."
}

# Add missing owner defaults to an existing .env without overwriting values.
ensure_owner_env_defaults() {
  add_default_if_missing() {
    local key="$1"
    local value="$2"
    if ! grep -q "^${key}=" "${N8N_ENV}"; then
      echo "${key}=${value}" >> "${N8N_ENV}"
      echo "Added ${key} to ${N8N_ENV}"
    fi
  }
  add_default_if_missing "N8N_OWNER_EMAIL" "admin@localhost.local"
  add_default_if_missing "N8N_OWNER_PASSWORD" "LocalDev123!"
  add_default_if_missing "N8N_OWNER_FIRST_NAME" "Local"
  add_default_if_missing "N8N_OWNER_LAST_NAME" "Admin"
}

load_env() {
  set -a
  # shellcheck disable=SC1090
  source "${N8N_ENV}"
  set +a
}

wait_for_n8n() {
  echo "Waiting for n8n to be ready..."
  for _ in $(seq 1 90); do
    if curl -sf "${N8N_URL}/healthz/readiness" >/dev/null 2>&1; then
      # Settings endpoint should return JSON once the editor API is up.
      if curl -sf "${N8N_URL}/rest/settings" | python3 -c "import sys,json; json.load(sys.stdin)" >/dev/null 2>&1; then
        return 0
      fi
    fi
    sleep 1
  done
  echo "n8n did not become ready in time." >&2
  exit 1
}

setup_needed() {
  local flag
  flag="$(curl -sf "${N8N_URL}/rest/settings" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('userManagement',{}).get('showSetupOnFirstLoad', False))" \
    2>/dev/null || true)"
  [[ "${flag}" == "True" || "${flag}" == "true" ]]
}

auto_create_owner() {
  if ! setup_needed; then
    echo "Owner already configured — skipping /setup."
    return
  fi

  if [[ -z "${N8N_OWNER_EMAIL:-}" || -z "${N8N_OWNER_PASSWORD:-}" ]]; then
    echo "Owner setup required but N8N_OWNER_EMAIL / N8N_OWNER_PASSWORD are missing in ${N8N_ENV}." >&2
    exit 1
  fi

  echo "Creating local n8n owner automatically (skipping /setup)..."
  local response http_code
  response="$(curl -sS -w "\n%{http_code}" -X POST "${N8N_URL}/rest/owner/setup" \
    -H "Content-Type: application/json" \
    -d "$(python3 - <<PY
import json, os
print(json.dumps({
    "email": os.environ["N8N_OWNER_EMAIL"],
    "password": os.environ["N8N_OWNER_PASSWORD"],
    "firstName": os.environ.get("N8N_OWNER_FIRST_NAME", "Local"),
    "lastName": os.environ.get("N8N_OWNER_LAST_NAME", "Admin"),
}))
PY
)")"
  http_code="$(echo "${response}" | tail -n1)"
  body="$(echo "${response}" | sed '$d')"

  if [[ "${http_code}" != "200" && "${http_code}" != "201" ]]; then
    echo "Owner setup failed (HTTP ${http_code}): ${body}" >&2
    exit 1
  fi

  echo "Owner created: ${N8N_OWNER_EMAIL}"
}

ensure_env_file
ensure_owner_env_defaults
load_env

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
docker compose -p "${PROJECT_NAME}" -f "${N8N_COMPOSE}" up -d --force-recreate

wait_for_n8n
auto_create_owner

echo "Importing local-stack credentials (if any)..."
bash "${SCRIPT_DIR}/n8n-import-credentials.sh" || true

echo "Importing versioned workflows (if any)..."
bash "${SCRIPT_DIR}/n8n-import-workflows.sh" || true

echo "n8n ready: ${N8N_URL}"
echo "Login: ${N8N_OWNER_EMAIL} / (password from DevOps/Local/n8n/.env)"
echo "Local credentials seeded: Ollama, Postgres (app), PGVector (vectors)."
