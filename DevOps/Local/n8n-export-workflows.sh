#!/usr/bin/env bash
# Export all n8n workflows into DevOps/Local/n8n/workflows for git versioning.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_NAME="ai-agents-with-langchain-n8n"
OUT_DIR="${SCRIPT_DIR}/n8n/workflows"

if ! docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "n8n container ${CONTAINER_NAME} is not running. Start it first:" >&2
  echo "  npm run local:n8n:start" >&2
  exit 1
fi

mkdir -p "${OUT_DIR}"
# Keep README.md; replace only JSON exports
find "${OUT_DIR}" -maxdepth 1 -type f -name '*.json' -delete

echo "Exporting workflows from ${CONTAINER_NAME} ..."
docker exec "${CONTAINER_NAME}" sh -c 'rm -rf /tmp/n8n-export && mkdir -p /tmp/n8n-export && n8n export:workflow --backup --output=/tmp/n8n-export'
docker cp "${CONTAINER_NAME}:/tmp/n8n-export/." "${OUT_DIR}/"

python3 - <<PY
import json
from pathlib import Path
out = Path("${OUT_DIR}")
for path in sorted(out.glob("*.json")):
    data = json.loads(path.read_text())
    workflows = data if isinstance(data, list) else [data]
    for w in workflows:
        for key in ("pinData", "versionId", "meta", "tags"):
            w.pop(key, None)
        # Fresh imports should not force-active in regular n8n mode
        w["active"] = False
        name = (w.get("name") or path.stem).strip().lower().replace(" ", "-")
        target = out / f"{name}.json"
        target.write_text(json.dumps(w, indent=2) + "\n")
        if target.resolve() != path.resolve():
            path.unlink(missing_ok=True)
        print(f"saved {target.name}")
PY

echo "Exported workflows to ${OUT_DIR}"
echo "Commit that folder, then fresh n8n starts will auto-import them."
