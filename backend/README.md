# Clarifi Backend

FastAPI backend for Clarifi's agentic career workflow.

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

The backend auto-loads keys from `backend/.env` (preferred) and also checks workspace `.env`.

## Endpoints

- `GET /health`
- `POST /api/clarifi/query`
- `POST /api/clarifi/resume/upload`
- `POST /api/clarifi/gap-bridge`

## Optional Web Search Key

```bash
SERPER_API_KEY=your_key_here
```

If the key is missing, the backend automatically uses safe fallback resources.

## Optional LLM Synthesis Key

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

If no key is provided, summaries gracefully fall back to deterministic local synthesis.

### Request

```json
{ "prompt": "AI Ethicist for Space Tech" }
```

### Response

```json
{
  "mode": "market_pulse",
  "summary": "Live-signal mode activated...",
  "cards": [
    {
      "title": "AI Ethics in Frontier Tech — 2026 Snapshot",
      "url": "https://example.com/ai-ethics-space-tech",
      "platform_icon": "🌐",
      "price": "Free"
    }
  ]
}
```

## Resume Upload Example

```bash
curl -X POST http://localhost:8000/api/clarifi/resume/upload \
  -F "file=@/path/to/resume.pdf" \
  -F "dream_vibe=AI Product Leader"
```

## Gap Bridge Example

```bash
curl -X POST http://localhost:8000/api/clarifi/gap-bridge \
  -H "Content-Type: application/json" \
  -d '{"resume_id": "<resume-id>", "dream_vibe": "AI Product Leader"}'
```

## Module Overview

- `app/models.py`: all request/response contracts
- `app/router.py`: intent routing logic
- `app/knowledge_base.py`: local retrieval docs
- `app/search_adapter.py`: external search integration
- `app/resume_processing.py`: CV parsing and rewrite/missing-skill logic
- `app/session_store.py`: temporary resume context memory
- `app/orchestrator.py`: workflow coordinator
- `app/llm_adapter.py`: optional LLM summary synthesizer
- `app/main.py`: API transport layer

## Observability

- Request tracing middleware logs method, path, status, and duration.
- Query endpoint logs route mode and reason.
