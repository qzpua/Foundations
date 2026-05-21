# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. The name of this SaaS app is Plaris.

## Commands

**Setup:**
```bash
make setup                                # create .venv
source .venv/bin/activate && uv sync --all-groups
pre-commit install
```

**Run (Docker — recommended):**
```bash
make run          # docker compose with local DB profile
```

**Run (terminal, no Docker):**
```bash
make run_local    # fastapi dev server at advolut/ with PYTHONPATH=.
```


**Tests:**
```bash
pytest                            # all tests
pytest tests/test_chat_session.py # single test file
```
Integration tests (`tests/test_search.py`) only run when `OPENAI_API_KEY` is set.

**Lint / Format:**
```bash
ruff check .      # lint (line length 79, excludes tests/)
ruff format .     # format
```

**Infra (CDK):**
```bash
cd infra && cdk deploy --all    # local deploy (requires Docker)
```
Production deploys automatically via GitHub Actions on push.

---

## Pull Request Checklist

- **Never push directly to the main branch. All changes must go through a pull request and be reviewed before merging.**
- Run `pytest` and fix failing tests.
- Run `ruff` and fix linter issues (line length 79).
- If OpenAI calls are added or changed, add or update tests to mock clients.
- Update README when you change developer-facing commands (e.g., Makefile targets, env var names).

## Architecture

The repo has two independent Python packages plus CDK infra:

### `advolut/` — FastAPI application

Entry point: `advolut/src/main.py`. Imports use the package namespace `src.*` (e.g. `from src.chat import router`). The `pytest.ini_options` in `pyproject.toml` adds `advolut` to `PYTHONPATH` so tests can resolve `src.*`.

**Startup lifecycle** (`src/lifespan/service.py`):
1. `init_db_pool` — creates an `asyncpg` connection pool (local Neon or Aurora RDS, chosen by presence of `LOCAL_DB_PASSWORD`).
2. `init_phoenix_tracing` — registers Arize Phoenix / OpenTelemetry instrumentation (skipped if `PHOENIX_DISABLE=true`).
3. `ChatSession()` — single shared instance stored on `app.state.chat_session`.
4. `init_faq_index()` — pre-warms the FAQ LlamaIndex in a thread to avoid cold-start latency on the first FAQ query.

**Chat flow** (`src/chat/`):
- `chat_session.py` — `ChatSession` is a Pydantic model holding an `AsyncOpenAI` client (class-level singleton). `send_message()` calls `openai_client.responses.create(...)` with a stored prompt ID (`chat_settings.PROMPT_ID`) and loops over tool calls until a message response is returned. On new sessions, promos are fetched via `get_current_promos()` and injected directly into the session context message (no tool call needed).
- `agent_tools.py` — defines three agent tools registered in `AGENT_TOOLS`: `faq_lookup_tool` (LlamaIndex in-memory vector index over FAQ docs), `rag_product_tool` (vector search over campervans), `rag_campground_tool` (vector search over campgrounds). All tools use `AsyncOpenAI()`. The `get_current_promos()` function is still present but is called directly by `chat_session.py`, not exposed as an agent tool. The RAG tools call `search_similar_products/campgrounds` which uses LlamaIndex's `PGVectorStore`.
- `config.py` — `ChatConfig` holds `PROMPT_ID`, `MODEL_TYPE`, and `MAX_OUTPUT_TOKENS` (512); overridable via env.

**OpenAI call styles — all async:**
- `chat_session.py`: async `AsyncOpenAI().responses.create(...)` (streaming tool loop)
- `agent_tools.py`: async `AsyncOpenAI().responses.parse(..., text_format=...)` for query synthesis
- `search/service.py`: async `AsyncOpenAI().responses.parse(..., text_format=CampervanRecommendations)` for structured extraction

**Vector search** (`src/search/vector_search.py`):
- Uses LlamaIndex `PGVectorStore` with `hybrid_search=True` (pgvector + BM25).
- Index instances are `@lru_cache`-memoised per `(table_name, schema_name)`.
- Schema resolved per-request via a `ContextVar` (`src/database.py`) set by auth middleware; falls back to `VECTOR_DB_SCHEMA` env var (default: `campervan_rental_shop`).

**Multitenancy**: API key → `advolut_api_key` table → `table_name` (Postgres schema). Each client's vector data lives under its own schema. The `acquire()` context manager sets `search_path` per connection. `get_context()` caches the API key → schema lookup in-process for 5 minutes (TTL cache in `src/database.py`) to avoid bcrypt + DB overhead on every request.

**Docstrings**: Use numpydoc style.

### `data_loader/` — AWS Lambda for data ingestion

Entry: `data_loader/main.py`. Triggered by S3 events. S3 key format: `<client_id>/<dataset>/<file>` or `<dataset>/<file>`.

- `load/config.py` — `LoadConfig` drives dataset routing via `DATASET_CONFIG_JSON` (overridable env var). Built-in datasets: `products` (CSV → `products` table), `campgrounds` (CSV → `campgrounds` table), `insights` (TXT/CSV → `text_embeddings` table).
- `load/routing.py` — routes S3 keys to the appropriate loader.
- `load/csv_loader.py` / `load/text_loader.py` — load files, generate embeddings via OpenAI (`text-embedding-3-small`), write to pgvector. Uses `psycopg2` (not asyncpg).
- `transform/csv_transformer.py` — transforms raw CSV columns before embedding.

Lambda expects `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and retrieves `OPENAI_API_KEY` from SSM Parameter Store.

### `infra/` — AWS CDK (TypeScript)

CDK app deploying: ECS on EC2 service (FastAPI app, t3.small ASG), Lambda (data loader), Aurora Serverless v2 (pgvector), S3 bucket, SSM parameters. CI/CD via `.github/workflows/aws_cdk.yml`.

---

## Key environment variables

| Variable | Used by | Notes |
|---|---|---|
| `OPENAI_API_KEY` | app + lambda | Required |
| `LOCAL_DB_PASSWORD` | app | Presence switches to local Neon DB |
| `VECTOR_DB_SCHEMA` | app | Default tenant schema (`campervan_rental_shop`) |
| `AURORA_DB_HOST/NAME/USERNAME/PASSWORD` | app (prod) | Aurora RDS |
| `PHOENIX_DISABLE` | app | Set to `true` to skip tracing |
| `PHOENIX_REDACT` | app | Set to `true` to redact trace values |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | app | Phoenix collector endpoint |
| `DB_HOST/NAME/USER/PASSWORD` | lambda | psycopg2 connection |

## Conventions & pitfalls

- Do not change imports to relative paths — all imports use `src.*` absolute package paths.
- All OpenAI calls are async (`AsyncOpenAI`). Do not introduce synchronous `OpenAI()` clients in async contexts — it blocks the event loop.
- `text_format=` typed parsing is used in `responses.parse()` calls — preserve this; do not convert to plain `responses.create()`.
- Promos are injected into the session context message at session start (in `chat_session.py`), not via a tool call. Do not re-add a `recommend_promos_tool` agent tool.
- Adding a new dataset type requires updating `DATASET_CONFIG_JSON` in `data_loader/load/config.py`.
- Pre-commit hooks run `ruff` and `pytest` (via `.venv/bin/pytest`); fix lint and failing tests before committing.
