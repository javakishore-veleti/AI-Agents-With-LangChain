# n8n workflows

Commit workflow JSON files here. They are mounted into the n8n container at `/workflows`
and imported on `npm run local:n8n:start`.

## Update from the UI

```bash
npm run local:n8n:export-workflows
git add DevOps/Local/n8n/workflows
git commit -m "Update n8n workflows"
```

## Credentials

Workflow files reference credential **names/IDs** only. After a fresh n8n database,
re-create credentials in the UI and link them on each node.
