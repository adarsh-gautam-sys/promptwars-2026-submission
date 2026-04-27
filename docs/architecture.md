# Architecture — ElectionGuide AI

## System Overview

ElectionGuide AI follows a **3-tier architecture**:

1. **Frontend (SPA)** — Single-page HTML/JS/Tailwind app designed with Stitch MCP
2. **Backend (FastAPI)** — REST API powered by Google ADK + Gemini 2.5 Flash
3. **Session Layer** — InMemorySessionService (swappable to Firebase Firestore)

## Request Flow

```
User Input → Frontend (app.js) → POST /api/chat
    → FastAPI → ADK Runner → Gemini 2.5 Flash
        → Tool Selection (if needed) → FunctionTool → Structured Data
        → LLM Synthesizes Response
    → JSON Response → Frontend Renders Markdown
```

## Key Design Decisions

### 1. Single Agent Architecture
We use a single `root_agent` rather than multi-agent orchestration because:
- The domain is well-scoped (Indian elections only)
- Tool routing is handled natively by Gemini's function calling
- Reduces latency vs. agent-to-agent delegation

### 2. FunctionTools over RAG
We chose `FunctionTool` over RAG (Retrieval-Augmented Generation) because:
- Election data is **structured and static** (ECI rules don't change often)
- Tools provide **deterministic, curated responses**
- No vector database overhead or embedding costs
- Easier to test and validate accuracy

### 3. Stitch MCP for Frontend
The frontend was designed using Google's Stitch MCP tool to:
- Generate a professional, dark-themed UI with the "Civic Prism" design system
- Use Tailwind CSS via CDN for consistent styling
- Create a production-quality look without a build step

### 4. Session Management
- Default: `InMemorySessionService` for zero-config local development
- Production: Can switch to Firebase Firestore for persistence across Cloud Run instances
