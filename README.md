# agent-tools-service

Tool backend for a channel-agnostic AI agent. The same service is meant to sit behind a
chat assistant, a WhatsApp bot or a voice agent: the agent decides *what* to do, this
service does it against real systems, safely.

## What it does today

| Endpoint | Purpose | Status |
|---|---|---|
| `GET /health` | Liveness check | done |
| `GET /tools/order-status/{order_id}` | Tool the agent calls to look up an order | in progress |
| `POST /webhooks/post-call` | Receives the conversation summary when a call ends, with HMAC signature check and idempotency | in progress |

Also included: a resilient async HTTP client (timeouts, retries with exponential backoff),
structured JSON logging, and configuration through environment variables.

## Roadmap

1. **Tools backend** (this stage): FastAPI, async I/O, validation, webhooks, tests.
2. **Agent layer**: tool calling through an LLM gateway (LiteLLM) with model routing and
   fallback, an MCP server exposing the same tools, and RAG over a knowledge base.
3. **Channels**: web chat, WhatsApp, and voice over a phone number.
4. **Operations**: tracing, cost per conversation, evaluation of agent answers.

## Quickstart

```bash
uv sync
cp .env.example .env
uv run uvicorn tools_service.main:app --reload
```

Open http://localhost:8000/docs for the interactive API.

Run the tests:

```bash
uv run pytest
```

## Project layout

```
src/tools_service/
  main.py          app factory and lifespan (startup / shutdown)
  config.py        settings from environment variables
  log.py           structured JSON logging
  db.py            SQLite schema, seed data and queries
  models.py        request and response schemas
  security.py      webhook signature verification
  clients/http.py  resilient async HTTP client
  routers/         health, tools and webhook endpoints
scripts/           standalone learning and utility scripts
tests/             pytest suite
```
