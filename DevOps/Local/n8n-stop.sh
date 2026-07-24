#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ai-agents-with-langchain"
N8N_COMPOSE="${SCRIPT_DIR}/n8n/docker-compose.yaml"

echo "Stopping n8n..."
docker compose -p "${PROJECT_NAME}" -f "${N8N_COMPOSE}" down

echo "n8n stopped. (Postgres left running — stop it via local:containers:stop if needed.)"
