# ElectionGuide AI 🗳️

> **PromptWars 2026 — Election Process Education**
> An interactive AI assistant that helps users understand the Indian election process, powered by **Google ADK + Gemini 2.5 Flash**.

![Built with Google ADK](https://img.shields.io/badge/Google-ADK-blue?logo=google)
![Gemini 2.5 Flash](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-purple)
![Cloud Run](https://img.shields.io/badge/Deploy-Cloud%20Run-green?logo=google-cloud)
![Firebase](https://img.shields.io/badge/Session-Firebase-orange?logo=firebase)

---

## 🌟 Overview

ElectionGuide AI is a civic education platform designed to demystify India's election process for first-time voters, students, and curious citizens. Using the **Google Agent Development Kit (ADK)** framework, it orchestrates a Gemini 2.5 Flash-powered agent with **6 specialized tools** that provide structured, factual, and non-partisan information sourced from the Election Commission of India (ECI).

### Key Features
- **Interactive Q&A** — Ask anything about elections, voter registration, nomination, polling, or counting
- **6 Custom AI Tools** — Each tool maps to a core election domain (Timeline, Registration, Nomination, Polling, Counting, Eligibility)
- **Live Demo Mode** — Judges can watch the agent answer 6 pre-scripted questions sequentially, showcasing all tools
- **Premium Stitch-Designed UI** — Dark glassmorphism theme with Indian tricolor accents, built using Google Stitch MCP
- **Session Persistence** — InMemorySessionService (with optional Firebase Firestore upgrade)
- **Cloud Run Ready** — Containerized with Docker for one-click deployment

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User (Browser)                      │
│         Stitch-Designed SPA (HTML/CSS/JS + Tailwind)    │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (JSON)
                         ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Server (main.py)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Google ADK Runner                         │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │     root_agent (Gemini 2.5 Flash)           │  │  │
│  │  │  ┌─────────────┐ ┌─────────────────────┐   │  │  │
│  │  │  │System Prompt │ │  6 FunctionTools    │   │  │  │
│  │  │  │(Civic Expert)│ │  ┌─────────────────┐│   │  │  │
│  │  │  └─────────────┘ │  │get_election_     ││   │  │  │
│  │  │                  │  │  timeline         ││   │  │  │
│  │  │                  │  │get_voter_         ││   │  │  │
│  │  │                  │  │  registration     ││   │  │  │
│  │  │                  │  │get_nomination_    ││   │  │  │
│  │  │                  │  │  process          ││   │  │  │
│  │  │                  │  │get_polling_day_   ││   │  │  │
│  │  │                  │  │  guide            ││   │  │  │
│  │  │                  │  │get_vote_counting  ││   │  │  │
│  │  │                  │  │check_eligibility  ││   │  │  │
│  │  │                  │  └─────────────────┘││   │  │  │
│  │  │                  └─────────────────────┘│   │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │             InMemorySessionService                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
PromptWars2/
├── backend/
│   ├── main.py                 # FastAPI server + ADK Runner
│   ├── config.py               # Pydantic settings (env vars)
│   ├── requirements.txt        # Python dependencies
│   └── election_agent/
│       ├── __init__.py          # Package init (exports root_agent)
│       ├── agent.py             # ADK Agent definition
│       ├── tools.py             # 6 custom FunctionTools
│       └── prompts.py           # System prompt + demo queries
├── frontend/
│   ├── index.html              # SPA (Stitch MCP + Tailwind)
│   └── app.js                  # Chat logic, demo flow, topics
├── docs/
│   ├── architecture.md         # System architecture
│   ├── prompt_evolution.md     # Prompt engineering notes
│   └── tool_usage.md           # Tool descriptions
├── tests/
│   └── test_tools.py           # Unit tests for tools
├── .env.example                # Environment template
├── .gitignore
├── Dockerfile                  # Cloud Run container
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Google Gemini API key ([Get one free](https://aistudio.google.com/apikey))

### Setup
```bash
# Clone the repo
git clone https://github.com/adarsh-gautam-sys/PromptWars2.git
cd PromptWars2

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run locally
python backend/main.py
```

Visit **http://localhost:8000** to use the application.

---

## 🤖 AI Agent Design

### Model Selection
- **Gemini 2.5 Flash** — Chosen for its speed, cost-efficiency, and strong instruction-following capabilities
- Ideal for real-time chat with sub-2-second response times

### Prompt Engineering
The system prompt instructs the agent to:
1. Act as a **non-partisan civic educator** focused on India's election process
2. Always **call the appropriate tool** before answering domain questions
3. Present information with **structured formatting** (headers, bullet points, tables)
4. Never express political opinions or partisan views
5. Cite the **Election Commission of India (ECI)** as the authoritative source

### Custom Tools (6 FunctionTools)
| Tool | Domain | Key Data |
|------|--------|----------|
| `get_election_timeline` | Election calendar | 9-stage timeline, MCC, notifications |
| `get_voter_registration_info` | Voter enrollment | Forms 6/7/8, NVSP portal, requirements |
| `get_nomination_process` | Candidate filing | Eligibility, deposits, affidavit scrutiny |
| `get_polling_day_guide` | Election day | EVM/VVPAT, voter rights, procedures |
| `get_vote_counting_info` | Results | Counting rounds, NOTA, postal ballots |
| `check_voter_eligibility` | Eligibility check | Age, citizenship, NRI rules |

---

## 🔒 Security

- **API keys** stored in `.env`, never committed to git
- **Input validation** via Pydantic models (max 2000 chars)
- **CORS** configured for specific origins
- **Rate limiting** built into the config layer
- **No hardcoded secrets** in source code

---

## 📊 Google Services Used

| Service | Purpose |
|---------|---------|
| **Gemini 2.5 Flash** | LLM for reasoning and generation |
| **Google ADK** | Agent framework with tool orchestration |
| **Cloud Run** | Serverless container deployment |
| **Firebase** | Session persistence (Firestore) |
| **Stitch MCP** | UI design system ("Civic Prism" theme) |

---

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/ -v

# Test API endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I register to vote?", "session_id": "test1"}'
```

---

## 🚢 Deployment (Cloud Run)

```bash
# Build container
docker build -t electionguide-ai .

# Deploy to Cloud Run
gcloud run deploy electionguide-ai \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## 📝 License

Built for **PromptWars 2026** hackathon. Educational use only.

---

<p align="center">Made with ❤️ for Indian democracy 🇮🇳</p>
