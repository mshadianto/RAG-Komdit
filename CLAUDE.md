# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-Agent RAG System for Indonesian Audit Committee (Komite Audit) expertise. Uses 6 specialized expert agents to answer questions about audit committee governance, planning, regulatory compliance, and reporting. Includes AI Financial Analyst with McKinsey/Big4 persona for automated financial document analysis. Built with FastAPI backend, Streamlit frontend, dual-LLM architecture (Groq for responses, GLM for routing), and Supabase vector store with pgvector.

**Language**: Indonesian (prompts, responses, and UI are in Bahasa Indonesia)

## Commands

### Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
```

### Run backend
```bash
python -m backend.main
```
Backend runs at http://localhost:8000. Embedding model downloads lazily on first query.

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
Project is configured for Railway deployment via `railway.json` and `nixpacks.toml`. Backend uses Nixpacks builder; frontend uses separate `frontend/railway.toml`.

### Pre-download embedding model (optional)
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

## Architecture

### Multi-Agent System (`agents/orchestrator.py`)
- **AgentOrchestrator**: Main entry point that coordinates the query pipeline. Global instance: `orchestrator`
- **QueryRouter**: Uses LLM to route queries to appropriate expert agent(s). Returns JSON with `primary_agent`, `secondary_agents`, `reasoning`
- **ExpertAgent**: Base class for 6 specialized agents. Builds Indonesian system prompts from `AGENT_ROLES` config
- **ResponseSynthesizer**: Combines responses from multiple agents into coherent answer

Query flow:
1. Router analyzes query using GLM (glm-4-plus) and selects primary/secondary agents (max controlled by `max_agents` param). Falls back to Groq if `GLM_API_KEY` not set.
2. Orchestrator retrieves relevant context via `similarity_search()` (default threshold: 0.7, top_k: 5)
3. Gets conversation history for session context (last 5 messages)
4. Selected agents process query with context in sequence
5. Synthesizer combines multi-agent responses (or returns single agent response directly)
6. Saves conversation and agent logs to database

### Financial Analyst (`agents/financial_analyst.py`)
- **FinancialAnalyst**: AI Senior Financial Analyst with McKinsey & Big 4 Consulting persona
- Credentials: CFA Charterholder, CPA, 15+ years experience
- Specialization: Financial Statement Analysis, Corporate Valuation, Risk Assessment
- Output format: Structured JSON with executive_summary, financial_ratios, risk_assessment, recommendations
- Analysis types: `comprehensive`, `quick`, `ratio_only`
- Uses low temperature (0.3) for factual analysis

### Backend Components (`backend/`)
- **main.py**: FastAPI app with CORS enabled. Key endpoints:
  - `POST /query`: Process query through multi-agent system
  - `POST /upload`: Upload document (background processing)
  - `POST /analyze`: Run financial analysis (returns structured JSON)
  - `GET /documents`, `DELETE /documents/{id}`: Document CRUD
  - `GET /conversations/{session_id}`: Chat history
  - `POST /feedback`: Conversation feedback (1-5 rating)
  - `GET /statistics/documents`, `GET /statistics/agents`: Analytics
- **database.py**: Supabase client wrapper, handles documents, embeddings, conversations, agent logs
- **embeddings.py**: Sentence Transformers wrapper (all-MiniLM-L6-v2, 384 dimensions). Uses lazy loading - model downloads on first query, not at startup
- **llm_client.py**: Dual-LLM client - `GLMClient` for routing (Zhipu AI glm-4-plus via httpx), `LLMClient` for responses (Groq Llama 3.3 70B). Global instances: `glm_client`, `llm_client`
- **document_processor.py**: Extracts text from PDF/DOCX/TXT/XLSX, auto-detects category, generates embeddings. Supported formats in `SUPPORTED_FORMATS` dict

### Configuration (`config/`)
- **config.py**: Pydantic settings via `pydantic-settings`. Key exports:
  - `settings`: Settings singleton with all env vars
  - `AGENT_ROLES`: Dict defining 6 expert agents with name, description, expertise list
  - `SYSTEM_PROMPTS`: Prompts for `query_router` and `synthesizer`
  - `UPLOAD_DIR`, `PROCESSED_DIR`: Path objects under `config/data/` for file storage (auto-created)
- **database_schema.sql**: PostgreSQL schema with pgvector extension. Run in Supabase SQL Editor to initialize

### Frontend (`frontend/app.py`)
Streamlit app with 6 pages via `streamlit-option-menu` (Midnight Vault dark theme):
- **Beranda**: Landing page with system stats, expert agent cards, example queries
- **Konsultasi**: Query interface with agent display, conversation history, feedback
- **Dokumen**: Upload (PDF/DOCX/TXT/XLSX), list, filter, delete documents, analyze button
- **Analisis**: Financial analysis page with McKinsey/Big4 analyst badge, document selector, tabbed results (Executive Summary, Ratios, Risk, Recommendations), analysis history
- **Analitik**: Document stats charts, agent performance metrics via Plotly
- **Tentang**: System info, health check display

Session state: `session_id` (UUID), `conversation_history` (list of query/response dicts)

## Key Configuration

Environment variables in `.env`:
- `GROQ_API_KEY`: Required for LLM responses
- `GLM_API_KEY`: Optional for query routing (falls back to Groq if not set)
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`: Required for vector store
- `GROQ_MODEL`: Default `llama-3.3-70b-versatile`
- `GLM_MODEL`: Default `glm-4-plus`
- `CHUNK_SIZE`: Default `500`, `CHUNK_OVERLAP`: Default `50`
- `AGENT_TEMPERATURE`: Default `0.7`, `MAX_TOKENS`: Default `2000`
- `API_BASE_URL`: Frontend API target, default `http://localhost:8000`

## Database Tables (Supabase)
- `komite_audit_documents`: Document metadata (id, filename, file_type, file_size, category, status, total_chunks, tags, metadata)
- `komite_audit_embeddings`: Chunks with 384-dim vector embeddings. Uses HNSW index for fast similarity search
- `komite_audit_conversations`: Chat history with session_id, agents_used, context_documents, similarity_scores, feedback
- `agent_logs`: Agent execution metrics (execution_time_ms, tokens_used, status)
- `financial_analyses`: AI financial analysis results (document_id, session_id, analysis_type, analysis_result JSONB, overall_assessment, risk_level, processing_time_ms)

Key stored procedure: `search_komite_audit_embeddings(query_embedding, match_threshold, match_count, filter_document_ids)`

Views: `document_statistics`, `agent_performance`, `analysis_statistics`

## Agent Keys
When referencing agents in code: `charter_expert`, `planning_expert`, `financial_review_expert`, `regulatory_expert`, `banking_expert`, `reporting_expert`

## Important Patterns

### Async Pattern
All database operations and LLM calls are async. Use `await` when calling:
- `db.similarity_search()`, `db.create_conversation()`, `db.get_document()`, etc.
- `llm_client.generate_completion()`, `llm_client.generate_with_context()`
- `orchestrator.process_query()`, `financial_analyst.analyze_document()`

### Error Handling
- LLM routing failures fall back to `charter_expert` as default agent
- Query processing returns `{"success": False, "error": ...}` on failure
- Financial analysis returns a fallback JSON structure with `"error"` field on failure

## Global Instances

Import these for direct access to initialized components:
- `from agents.orchestrator import orchestrator` - Main query entry point
- `from agents.financial_analyst import financial_analyst` - Financial analysis
- `from backend.llm_client import llm_client, glm_client` - LLM clients
- `from backend.database import db` - Database operations
- `from backend.embeddings import embedding_manager` - Embeddings
- `from config.config import settings, AGENT_ROLES, SYSTEM_PROMPTS` - Configuration
