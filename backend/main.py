"""
ElectionGuide AI — FastAPI Server
Main entry point serving the API endpoints and static frontend.
"""

import os
import sys
import uuid
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

# ── Path setup ──────────────────────────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# Set the API key for google-genai before importing ADK
os.environ.setdefault("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))

from config import get_settings
from election_agent.agent import root_agent
from election_agent.prompts import DEMO_QUERIES, TOPIC_CARDS

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("electionguide")

# ── Session & Runner ────────────────────────────────────────────────────────
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="election_guide_ai",
    session_service=session_service,
)

# ── Rate Limiter (simple in-memory) ─────────────────────────────────────────
request_counts: dict[str, list[float]] = {}


# ── Lifespan ────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("🗳️  ElectionGuide AI starting on port %s", settings.port)
    logger.info("📡  Model: %s", settings.gemini_model)
    yield
    logger.info("👋  ElectionGuide AI shutting down")


# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ElectionGuide AI",
    description="Interactive election process education assistant powered by Google ADK + Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response Models ───────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: str = Field(default="", description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    response: str
    session_id: str
    tools_used: list[str] = []


# ── Helper: Run agent ──────────────────────────────────────────────────────

async def run_agent(user_message: str, session_id: str) -> tuple[str, list[str]]:
    """Send a message to the ADK agent and collect the response."""
    user_id = "user_web"

    # Ensure session exists — create if not found
    try:
        session = await session_service.get_session(
            app_name="election_guide_ai", user_id=user_id, session_id=session_id
        )
        if session is None:
            await session_service.create_session(
                app_name="election_guide_ai", user_id=user_id, session_id=session_id
            )
    except Exception:
        try:
            await session_service.create_session(
                app_name="election_guide_ai", user_id=user_id, session_id=session_id
            )
        except Exception:
            pass  # Session may already exist from a race condition

    content = types.Content(role="user", parts=[types.Part(text=user_message)])

    response_parts = []
    tools_used = []

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_parts.append(part.text)
        # Track tool usage
        if hasattr(event, 'function_calls') and event.function_calls:
            for fc in event.function_calls:
                if hasattr(fc, 'name'):
                    tools_used.append(fc.name)

    full_response = "\n".join(response_parts) if response_parts else "I'm sorry, I couldn't generate a response. Please try again."
    return full_response, tools_used


# ── API Endpoints ───────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy", "service": "ElectionGuide AI", "model": settings.gemini_model}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Send a message to the election guide agent."""
    session_id = request.session_id or str(uuid.uuid4())

    try:
        response_text, tools_used = await run_agent(request.message, session_id)
        tool_used = tools_used[0] if tools_used else None
        return {
            "response": response_text,
            "session_id": session_id,
            "tools_used": tools_used,
            "tool_used": tool_used,
        }
    except Exception as e:
        logger.error("Chat error: %s", str(e))
        return JSONResponse(status_code=500, content={"error": f"Agent error: {str(e)}"})


class DemoRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Demo question")
    step: int = Field(default=0, description="Demo step index")


# Persistent demo session
_demo_session_id: str = ""


@app.post("/api/demo")
async def run_demo(request: DemoRequest):
    """Run a single demo step — the frontend sends questions one at a time."""
    global _demo_session_id

    # Create a new session for step 0
    if request.step == 0:
        _demo_session_id = f"demo_{uuid.uuid4().hex[:8]}"

    session_id = _demo_session_id or f"demo_{uuid.uuid4().hex[:8]}"

    try:
        response_text, tools_used = await run_agent(request.question, session_id)
        tool_used = tools_used[0] if tools_used else None
        return {
            "response": response_text,
            "tool_used": tool_used,
            "tools_used": tools_used,
            "step": request.step,
        }
    except Exception as e:
        logger.error("Demo error at step %d: %s", request.step, str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/topics")
async def get_topics():
    """Return the list of quick-access topic cards."""
    return {"topics": TOPIC_CARDS}


# ── Static Frontend Serving ─────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets") if os.path.isdir(os.path.join(FRONTEND_DIR, "assets")) else None
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "ElectionGuide AI API is running. Frontend not found.", "docs": "/docs"}


# ── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
