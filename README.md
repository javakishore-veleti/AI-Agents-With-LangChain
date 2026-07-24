# AI-Agents-With-LangChain

Local tutorials and DevOps helpers for LangChain / LangGraph / agent workflows.

## Local containers

From the repo root:

```bash
npm run local:containers:start
npm run local:containers:status
npm run local:containers:stop
```

These manage the shared Compose project `ai-agents-with-langchain`:

| Service | Container | Port |
|---------|-----------|------|
| ChromaDB | `ai-agents-with-langchain-chromadb` | 8000 |
| MongoDB | `ai-agents-with-langchain-mongodb` | 27017 |
| Postgres | `ai-agents-with-langchain-postgres` | 5432 |
| PgVector | `ai-agents-with-langchain-pgvector` | 5433 |

## n8n (opt-in)

n8n is **not** started by `local:containers:*`. Start it only when needed:

```bash
npm run local:n8n:start
npm run local:n8n:status
npm run local:n8n:stop
```

- UI: http://localhost:5678
- Uses Postgres DB `n8n` on `ai-agents-with-langchain-postgres`
- Owner account is created automatically on first start (skips `/setup`)

### Local login

| Field | Value |
|-------|--------|
| URL | http://localhost:5678 |
| Email | `admin@localhost.local` |
| Password | `LocalDev123!` |

These defaults live in `DevOps/Local/n8n/.env` (gitignored) and `DevOps/Local/n8n/.env.example`.

Change them in `.env` before the first `npm run local:n8n:start` if you want different credentials. Do not change `N8N_ENCRYPTION_KEY` after you have saved credentials in n8n.
