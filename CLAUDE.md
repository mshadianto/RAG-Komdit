# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-Agent RAG System for Indonesian Audit Committee (Komite Audit) expertise. Uses 7 specialized expert agents to answer questions about audit committee governance, planning, regulatory compliance, reporting, and ESG/sustainability. Includes AI Financial Analyst (CFA/CPA Senior Analyst persona) for automated financial document analysis. Built with FastAPI backend, Streamlit frontend, dual-LLM architecture (Groq for responses, GLM for routing), and Supabase vector store with pgvector.

**Language**: Indonesian (prompts, responses, and UI are in Bahasa Indonesia)

## Commands

### Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r dev-requirements.txt   # All deps (backend + frontend + tools)
cp .env.example .env                  # Then fill in API keys
```
Note: `requirements.txt` is for Docker/production. Use `dev-requirements.txt` for local development (includes Streamlit, Plotly, etc.).

### Run backend
```bash
python -m backend.main
```
Backend runs at http://localhost:8000. Embedding model downloads lazily on first query. Uses `python -m` to ensure correct module resolution without setting `PYTHONPATH`.

### Run frontend
```bash
streamlit run frontend/app.py
```
Frontend runs at http://localhost:8501 (connects to `API_BASE_URL`, default http://localhost:8000)

### Run tests
```bash
pytest tests/                                    # All tests
pytest tests/test_embeddings.py                  # Single test file
pytest tests/test_embeddings.py -k "test_name"   # Single test function
```

### Deployment (Railway)
Backend uses `railway.json` with Dockerfile builder; frontend uses `frontend/railway.toml` with Nixpacks builder. Docker sets `PYTHONPATH=/app` for module imports.

### Pre-download embedding model (optional)
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

## Architecture

### Query Flow
1. **QueryRouter** analyzes query using GLM (glm-4-plus) and selects primary/secondary agents (max controlled by `max_agents` param). Falls back to Groq if `GLM_API_KEY` not set.
2. **AgentOrchestrator** retrieves relevant context via `similarity_search()` (default threshold: 0.7, top_k: 5) and conversation history (last 5 messages).
3. Selected **ExpertAgent**(s) process query with context in sequence. Each agent builds Indonesian system prompts from `AGENT_ROLES` config.
4. **ResponseSynthesizer** combines multi-agent responses (or returns single agent response directly).
5. Saves conversation and agent logs to database.

### Dual-LLM Architecture
- **GLMClient** (`backend/llm_client.py`): Zhipu AI glm-4-plus via httpx for query routing (cheaper). Falls back to Groq if `GLM_API_KEY` not set.
- **LLMClient** (`backend/llm_client.py`): Groq Llama 3.3 70B for agent responses. Wraps Groq Python SDK.

### Financial Analyst (`agents/financial_analyst.py`)
AI Senior Financial Analyst persona (CFA/CPA). Uses low temperature (0.3), max 4000 tokens, JSON mode. Analysis types: `comprehensive`, `quick`, `ratio_only`. Output: structured JSON with executive_summary, financial_ratios, risk_assessment, recommendations, data_quality_notes.

### Risk-Audit Mapper (`agents/risk_audit_mapper.py`)
Senior Risk & Audit Strategy Consultant persona (CIA/CRMA). Maps Risk Register against PKPT (audit plan) to identify coverage gaps. Uses low temperature (0.3), max 4000 tokens, JSON mode. Accepts TWO documents (risk register + audit plan, each truncated to 25k chars). Mapping types: `comprehensive`, `quick`, `gap_only`. Output: structured JSON with executive_summary, risk_register_summary, audit_plan_summary, coverage_matrix, gap_analysis, recommendations, data_quality_notes. Endpoints: `POST /risk-mapping`, `GET /risk-mappings`, `GET /risk-mappings/{mapping_id}`.

### Backend (`backend/`)
- **main.py**: FastAPI app with CORS. Key endpoints: `/query`, `/upload`, `/analyze`, `/documents`, `/conversations/{session_id}`, `/feedback`, `/statistics/*`, `/agents`
- **database.py**: Supabase client (uses `SUPABASE_SERVICE_KEY`). Batch embedding insertion (100/batch). Calls `search_komite_audit_embeddings()` stored procedure.
- **embeddings.py**: Sentence Transformers (all-MiniLM-L6-v2, 384 dims). Lazy loading via `@property` — model loads on first use, not at startup.
- **document_processor.py**: Extracts text from PDF/DOCX/TXT/XLSX, auto-detects category, chunks text, generates embeddings. Background processing via FastAPI `BackgroundTasks`.

### Configuration (`config/`)
- **config.py**: Pydantic settings from `.env`. Exports: `settings`, `AGENT_ROLES` (7 agents), `SYSTEM_PROMPTS` (router + synthesizer), `UPLOAD_DIR`/`PROCESSED_DIR` (auto-created under `config/data/`).
- **database_schema.sql**: PostgreSQL schema with pgvector. Run in Supabase SQL Editor to initialize.

### Frontend (`frontend/app.py`)
Streamlit app with 7 pages (Beranda, Konsultasi, Dokumen, Analisis, Risk Mapping, Analitik, Tentang). Uses `streamlit-option-menu` and Midnight Vault dark theme. Session state: `session_id` (UUID), `conversation_history`.

## Key Configuration

Environment variables in `.env` (copy from `.env.example`):
- `GROQ_API_KEY`: **Required** for LLM responses
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`: **Required** for vector store
- `GLM_API_KEY`: Optional for query routing (falls back to Groq)
- `GROQ_MODEL`: Default `llama-3.3-70b-versatile`
- `GLM_MODEL`: Default `glm-4-plus`
- `API_BASE_URL`: Frontend API target, default `http://localhost:8000`
- `ENVIRONMENT`: `development` (enables uvicorn reload) or `production`

Note: `.env.example` shows `GROQ_MODEL=llama-3.1-70b-versatile` but the actual default in `config.py` is `llama-3.3-70b-versatile`.

## Tuning Defaults

These values are hardcoded in the orchestrator/agents and affect query behavior:
- Similarity threshold: 0.7, top_k: 5 (in `orchestrator.retrieve_context()`)
- Conversation history: last 5 messages per session
- Embedding batch insert: 100 per batch
- Financial analyst: temperature 0.3, max 4000 tokens, JSON mode
- Risk-audit mapper: temperature 0.3, max 4000 tokens, JSON mode, 25k chars per doc
- Agent responses: temperature from `settings.AGENT_TEMPERATURE` (0.7), max from `settings.MAX_TOKENS` (2000)

## Database (Supabase)

Tables: `komite_audit_documents`, `komite_audit_embeddings` (384-dim vectors, HNSW index), `komite_audit_conversations`, `agent_logs`, `financial_analyses`, `risk_audit_mappings`

Key stored procedure: `search_komite_audit_embeddings(query_embedding, match_threshold, match_count, filter_document_ids)`

Views: `document_statistics`, `agent_performance`, `analysis_statistics`, `risk_mapping_statistics`

## Agent Keys
`charter_expert`, `planning_expert`, `financial_review_expert`, `regulatory_expert`, `banking_expert`, `reporting_expert`, `esg_expert`, `risk_mapping_expert`

## Important Patterns

### Async Pattern
All database operations and LLM calls are async. Use `await` when calling:
- `db.similarity_search()`, `db.create_conversation()`, `db.get_document()`, etc.
- `llm_client.generate_completion()`, `llm_client.generate_with_context()`
- `orchestrator.process_query()`, `financial_analyst.analyze_document()`, `risk_audit_mapper.analyze_mapping()`

### Error Handling
- LLM routing failures fall back to `charter_expert` as default agent
- Query processing returns `{"success": False, "error": ...}` on failure
- Financial analysis returns a fallback JSON structure with `"error"` field on failure

### Global Instances
```python
from agents.orchestrator import orchestrator       # Main query entry point
from agents.financial_analyst import financial_analyst  # Financial analysis
from agents.risk_audit_mapper import risk_audit_mapper  # Risk-audit mapping
from backend.llm_client import llm_client, glm_client  # LLM clients
from backend.database import db                    # Database operations
from backend.embeddings import embedding_manager   # Embeddings
from config.config import settings, AGENT_ROLES, SYSTEM_PROMPTS  # Configuration
```
