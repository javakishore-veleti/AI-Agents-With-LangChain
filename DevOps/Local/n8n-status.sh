#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ai-agents-with-langchain"
N8N_COMPOSE="${SCRIPT_DIR}/n8n/docker-compose.yaml"

echo "Project: ${PROJECT_NAME}"
echo "=== n8n ==="
docker compose -p "${PROJECT_NAME}" -f "${N8N_COMPOSE}" ps
echo
echo "=== Postgres (n8n DB host) ==="
docker ps --filter name=ai-agents-with-langchain-postgres --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
