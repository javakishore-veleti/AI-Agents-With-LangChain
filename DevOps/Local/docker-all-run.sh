#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIRS=("ChromDB" "MongoDB")

for dir in "${COMPOSE_DIRS[@]}"; do
  compose_file="${SCRIPT_DIR}/${dir}/docker-compose.yaml"
  echo "Starting containers in ${dir}..."
  docker compose -f "${compose_file}" up -d
done

echo "All local containers started."
