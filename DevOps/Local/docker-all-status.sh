#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ai-agents-with-langchain"
COMPOSE_DIRS=("ChromDB" "MongoDB" "Postgres" "PgVector")

echo "Project: ${PROJECT_NAME}"
echo

for dir in "${COMPOSE_DIRS[@]}"; do
  compose_file="${SCRIPT_DIR}/${dir}/docker-compose.yaml"
  echo "=== ${dir} ==="
  docker compose -p "${PROJECT_NAME}" -f "${compose_file}" ps
  echo
done
