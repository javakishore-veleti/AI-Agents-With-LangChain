#!/usr/bin/env bash
# Import local-stack credentials (Postgres / PGVector / Ollama) into n8n.
set -euo pipefail

CONTAINER_NAME="ai-agents-with-langchain-n8n"

if ! docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "n8n container ${CONTAINER_NAME} is not running." >&2
  exit 1
fi

if ! docker exec "${CONTAINER_NAME}" sh -c 'test -f /credentials/local-stack.json'; then
  echo "No /credentials/local-stack.json mounted; skipping credential import."
  exit 0
fi

echo "Importing local Docker-stack credentials into n8n..."
docker exec "${CONTAINER_NAME}" n8n import:credentials --input=/credentials/local-stack.json
echo "Credential import finished."
