# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-Agent RAG System for Indonesian Audit Committee (Komite Audit) expertise. Uses 6 specialized expert agents to answer questions about audit committee governance, planning, regulatory compliance, and reporting. Built with FastAPI backend, Streamlit frontend, Groq LLM, and Supabase vector store.

## Commands

### Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
```

### Download embedding model (first time only)
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### Run backend
```bash
python -m backend.main
```
Backend runs at http://localhost:8000

### Run frontend
```bash
streamlit run frontend/app.py
```
Frontend runs at http://localhost:8501 (configurable via `API_BASE_URL` env var)

### Run tests
```bash
pytest tests/
```

### Deployment (Railway)
Project is configured for Railway deployment via `railway.json` and `nixpacks.toml`. Backend uses Nixpacks builder; frontend uses separate `frontend/railway.toml`.

## Architecture

### Multi-Agent System (`agents/orchestrator.py`)
- **AgentOrchestrator**: Main entry point that coordinates the query pipeline. Global instance: `orchestrator`
- **QueryRouter**: Uses LLM to route queries to appropriate expert agent(s). Returns JSON with `primary_agent`, `secondary_agents`, `reasoning`
- **ExpertAgent**: Base class for 6 specialized agents. Builds Indonesian system prompts from `AGENT_ROLES` config
- **ResponseSynthesizer**: Combines responses from multiple agents into coherent answer

Query flow:
1. Router analyzes query using GLM (glm-4-flash) and selects primary/secondary agents (max controlled by `max_agents` param). Falls back to Groq if GLM not configured.
2. Orchestrator retrieves relevant context via `similarity_search()` (default threshold: 0.7, top_k: 5)
3. Gets conversation history for session context (last 5 messages)
4. Selected agents process query with context in sequence
5. Synthesizer combines multi-agent responses (or returns single agent response directly)
6. Saves conversation and agent logs to database

### Backend Components (`backend/`)
- **main.py**: FastAPI app with CORS enabled. Endpoints:
  - `GET /`, `GET /health`: Health checks
  - `POST /query`: Process query through multi-agent system
  - `POST /upload`: Upload document (background processing)
  - `GET /documents`, `GET /documents/{id}`, `DELETE /documents/{id}`: Document CRUD
  - `GET /conversations/{session_id}`: Get chat history
  - `POST /feedback`: Submit conversation feedback (1-5 rating)
  - `GET /statistics/documents`, `GET /statistics/agents`: Analytics
  - `GET /agents`: List available expert agents
- **database.py**: Supabase client wrapper, handles documents, embeddings, conversations, agent logs
- **embeddings.py**: Sentence Transformers wrapper (all-MiniLM-L6-v2, 384 dimensions). Uses lazy loading - model downloads on first query, not at startup
- **llm_client.py**: Dual-LLM client - GLM/Zhipu AI for routing (glm-4-flash), Groq for responses (Llama 3.1 70B)
- **document_processor.py**: Extracts text from PDF/DOCX/TXT/XLSX, auto-detects category, generates embeddings. Supported formats defined in `SUPPORTED_FORMATS` dict

### Configuration (`config/`)
- **config.py**: Pydantic settings via `pydantic-settings`. Key exports:
  - `settings`: Settings singleton with all env vars
  - `AGENT_ROLES`: Dict defining 6 expert agents with name, description, expertise list
  - `SYSTEM_PROMPTS`: Prompts for `query_router` and `synthesizer`
  - `UPLOAD_DIR`, `PROCESSED_DIR`: Path objects for file storage
- **database_schema.sql**: PostgreSQL schema with pgvector extension. Run in Supabase SQL Editor to initialize

### Frontend (`frontend/app.py`)
Streamlit app with 4 pages via `streamlit-option-menu`:
- **Chat**: Query interface with agent display, conversation history, feedback
- **Documents**: Upload (PDF/DOCX/TXT/XLSX), list, filter, delete documents
- **Analytics**: Document stats charts, agent performance metrics via Plotly
- **About**: System info, health check display

Session state: `session_id` (UUID), `conversation_history` (list of query/response dicts)

## Key Configuration

Environment variables in `.env`:
- `GROQ_API_KEY`: Required for LLM responses
- `GLM_API_KEY`: Required for query routing (Zhipu AI)
- `GLM_MODEL`: Default `glm-4-flash`
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`: Required for vector store
- `GROQ_MODEL`: Default `llama-3.1-70b-versatile`
- `EMBEDDING_MODEL`: Default `sentence-transformers/all-MiniLM-L6-v2`
- `VECTOR_DIMENSION`: Default `384`
- `CHUNK_SIZE`: Default `500`
- `CHUNK_OVERLAP`: Default `50`
- `AGENT_TEMPERATURE`: Default `0.7`
- `MAX_TOKENS`: Default `2000`
- `ENVIRONMENT`: Default `development`
- `LOG_LEVEL`: Default `INFO`
- `API_BASE_URL`: Frontend API target, default `http://localhost:8000`

## Database Tables (Supabase)
- `komite_audit_documents`: Document metadata (id, filename, file_type, file_size, category, status, total_chunks, tags, metadata)
- `komite_audit_embeddings`: Chunks with 384-dim vector embeddings. Uses HNSW index for fast similarity search
- `komite_audit_conversations`: Chat history with session_id, agents_used, context_documents, similarity_scores, feedback
- `agent_logs`: Agent execution metrics (execution_time_ms, tokens_used, status)

Key stored procedure: `search_komite_audit_embeddings(query_embedding, match_threshold, match_count, filter_document_ids)`

Views: `document_statistics`, `agent_performance`

## Agent Keys
When referencing agents in code: `charter_expert`, `planning_expert`, `financial_review_expert`, `regulatory_expert`, `banking_expert`, `reporting_expert`

## File Structure
```
rag-komdit/
├── agents/orchestrator.py     # Multi-agent system
├── backend/
│   ├── main.py                # FastAPI endpoints
│   ├── database.py            # Supabase client
│   ├── embeddings.py          # Sentence Transformers (lazy loading)
│   ├── llm_client.py          # Groq API client
│   └── document_processor.py  # Document parsing
├── config/
│   ├── config.py              # Settings & agent definitions
│   ├── database_schema.sql    # Supabase schema
│   └── data/                  # uploads/ and processed/ dirs
├── frontend/
│   ├── app.py                 # Streamlit UI
│   └── railway.toml           # Frontend Railway config
├── tests/test_embeddings.py   # Embedding tests
├── download_model.py          # Pre-download model for Railway build
├── requirements.txt
├── railway.json               # Railway deployment config
├── nixpacks.toml              # Nixpacks build config
└── .env                       # Environment variables
```
