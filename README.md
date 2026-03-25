# Clarifi

Ultra-modern, Gemini-inspired **full-stack** interface for Clarifi with an agentic backend workflow.

## What’s Included

- Left vertical icon sidebar (`Home`, `History`, `Settings`)
- Top-left Clarifi branding with glowing prism mark
- Center hero heading:
	- **"Hey there! Where should we take your career today?"**
- Four suggested prompt cards
- Bottom rounded command bar with animated gradient glow
- Resume upload flow (`PDF`, `DOCX`, `TXT`) for Resume Glow-Up
- Gap Bridge trigger for missing-skill learning paths
- Responsive layout for desktop + mobile widths

## Tech Stack

- React 17
- Vite 2
- CSS (custom styling + animations)
- FastAPI + Pydantic (backend)

## Quick Start

```bash
npm install
npm run dev
```

Open frontend: `http://localhost:3000`

To use real API responses (instead of fallback mock), run the backend too:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Optional frontend env:

```bash
cp .env.example .env
```

Optional backend search env:

```bash
export SERPER_API_KEY=your_key_here
```

Optional backend LLM synthesis env:

```bash
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-4o-mini
```

## Build Check

```bash
npm run build
```

This creates optimized files in `dist/`.

## Deploy to Production

Ready to go live? Follow [DEPLOYMENT.md](DEPLOYMENT.md) for:
- **Vercel + Railway** (easiest, recommended)
- **Docker** (self-hosted or cloud)
- **Environment variable setup**
- **Troubleshooting**

## Test the Interface First (Manual QA)

Use this checklist before adding backend/AI logic:

### 1) Initial Load

- [ ] Page loads without errors
- [ ] Background shows deep midnight tone with animated aurora glows (teal/lavender/orange)
- [ ] No layout overflow or clipped content

### 2) Branding + Navigation

- [ ] `Clarifi` branding appears at top-left
- [ ] Prism icon appears with subtle glow
- [ ] Sidebar shows 3 icon-only controls
- [ ] Sidebar icons highlight softly on hover

### 3) Main Content

- [ ] Hero title is centered and readable
- [ ] Four prompt cards are visible and evenly spaced
- [ ] Prompt cards have semi-transparent/frosted look
- [ ] Card hover feels smooth and minimal

### 4) Command Bar

- [ ] Command bar stays near bottom center
- [ ] Gradient ring/glow pulses subtly
- [ ] Placeholder text is visible and legible
- [ ] Send button appears and reacts on hover

### 5) Responsive Check

- [ ] At narrow width (mobile), brand text hides but icon remains
- [ ] Prompt cards stack into one column
- [ ] Input bar remains usable without overlap

## Suggested Browser Test Matrix

- Chrome (latest)
- Edge (latest)
- Firefox (latest)

## Project Structure

```text
index.html
src/
	App.jsx
	main.jsx
	styles.css
vite.config.ts
```

## API Flows

### 1) Query Router

- Endpoint: `POST /api/clarifi/query`
- Router mode output: `career_guide`, `market_pulse`, `resume_glowup`, `gap_bridge`
- Returns structured JSON (`mode`, `summary`, `cards[]`) for clean UI cards.

### 2) Resume Glow-Up

- Endpoint: `POST /api/clarifi/resume/upload`
- Multipart input: `file`, `dream_vibe`
- Returns: `resume_id`, `rewrites[]`, `missing_skills[]`, and card recommendations.

### 3) Gap Bridge

- Endpoint: `POST /api/clarifi/gap-bridge`
- Input: `resume_id`, `dream_vibe`
- Returns top learning cards for missing skills.

## Architecture (Beginner View)

- `router.py`: decides which workflow to run based on user intent.
- `knowledge_base.py`: local evergreen guidance (RAG-lite retrieval).
- `search_adapter.py`: web-search adapter (Serper when key exists, safe fallback when not).
- `resume_processing.py`: parses CV and generates rewrite + missing-skill signals.
- `session_store.py`: keeps uploaded resume context in-memory for follow-up requests.
- `orchestrator.py`: coordinates all modules and returns consistent frontend JSON.
- `llm_adapter.py`: optional live LLM summary generation with fallback when API key is missing.

## Tracing

- API logs request timing and path for each call.
- Query logs include route decision (`mode` + `reason`) so you can debug router behavior.
