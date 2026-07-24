#!/usr/bin/env bash
# Import committed workflow JSON files into the running n8n container.
set -euo pipefail

CONTAINER_NAME="ai-agents-with-langchain-n8n"

if ! docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "n8n container ${CONTAINER_NAME} is not running." >&2
  exit 1
fi

if ! docker exec "${CONTAINER_NAME}" sh -c 'ls /workflows/*.json >/dev/null 2>&1'; then
  echo "No workflow JSON files found in /workflows (mount DevOps/Local/n8n/workflows)."
  exit 0
fi

echo "Importing workflows from /workflows ..."
# Imported workflows start inactive in regular mode; activate in the UI if needed.
docker exec "${CONTAINER_NAME}" n8n import:workflow --separate --input=/workflows
echo "Workflow import finished."
