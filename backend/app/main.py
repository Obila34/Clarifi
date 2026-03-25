import logging
import time
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from .models import GapBridgeRequest, GapBridgeResponse, QueryRequest, QueryResponse, ResumeUploadResponse
from .orchestrator import ClarifiOrchestrator
from .router import route_mode
from .session_store import InMemorySessionStore


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("clarifi.api")

backend_dir = Path(__file__).resolve().parents[1]
workspace_dir = backend_dir.parent
load_dotenv(backend_dir / ".env", override=False)
load_dotenv(workspace_dir / ".env", override=False)


app = FastAPI(title="Clarifi API", version="0.1.0")
store = InMemorySessionStore()
orchestrator = ClarifiOrchestrator(store=store)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def trace_requests(request: Request, call_next):
    request_id = str(uuid4())
    start = time.perf_counter()

    response: Response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-Id"] = request_id
    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/clarifi/query", response_model=QueryResponse)
async def clarifi_query(payload: QueryRequest) -> QueryResponse:
    decision = route_mode(payload.prompt)
    logger.info(
        "route_decision mode=%s reason=%s prompt=%s",
        decision.mode,
        decision.reason,
        payload.prompt,
    )
    return await orchestrator.handle_query(prompt=payload.prompt, decision=decision)


@app.post("/api/clarifi/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    dream_vibe: str = Form("AI Career Transition"),
) -> ResumeUploadResponse:
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        return orchestrator.process_resume_upload(
            filename=file.filename or "resume.txt",
            file_bytes=file_bytes,
            dream_vibe=dream_vibe,
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/clarifi/gap-bridge", response_model=GapBridgeResponse)
async def gap_bridge(payload: GapBridgeRequest) -> GapBridgeResponse:
    try:
        return await orchestrator.build_gap_bridge(
            resume_id=payload.resume_id,
            dream_vibe=payload.dream_vibe,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
