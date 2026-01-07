# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-Agent RAG System for Indonesian Audit Committee (Komite Audit) expertise. Uses 6 specialized expert agents to answer questions about audit committee governance, planning, regulatory compliance, and reporting.

## Commands

### Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### Download embedding model
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

### Run tests
```bash
pytest tests/
```

## Architecture

### Multi-Agent System (`agents/orchestrator.py`)
- **AgentOrchestrator**: Main entry point that coordinates the query pipeline
- **QueryRouter**: Uses LLM to route queries to appropriate expert agent(s)
- **ExpertAgent**: Base class for 6 specialized agents (charter, planning, financial_review, regulatory, banking, reporting)
- **ResponseSynthesizer**: Combines responses from multiple agents into coherent answer

Query flow:
1. Router analyzes query and selects primary/secondary agents
2. Orchestrator retrieves relevant context via vector similarity search
3. Selected agents process query with context
4. Synthesizer combines multi-agent responses

### Backend Components (`backend/`)
- **main.py**: FastAPI app with REST endpoints (/query, /upload, /documents, /statistics)
- **database.py**: Supabase client wrapper, handles documents, embeddings, conversations
- **embeddings.py**: Sentence Transformers wrapper (all-MiniLM-L6-v2, 384 dimensions)
- **llm_client.py**: Groq API client (Llama 3.1 70B)
- **document_processor.py**: Extracts text from PDF/DOCX/TXT/XLSX, auto-detects category, generates embeddings

### Configuration (`config/`)
- **config.py**: Pydantic settings, agent role definitions, system prompts
- **database_schema.sql**: PostgreSQL schema with pgvector extension for Supabase

### Frontend (`frontend/app.py`)
Streamlit app with Chat, Documents, Analytics, and About pages.

## Key Configuration

Environment variables in `.env`:
- `GROQ_API_KEY`: Required for LLM
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`: Required for vector store
- `CHUNK_SIZE=500`, `CHUNK_OVERLAP=50`: Document chunking parameters
- `AGENT_TEMPERATURE=0.7`, `MAX_TOKENS=2000`: LLM parameters

## Database Tables (Supabase)
- `komite_audit_documents`: Document metadata
- `komite_audit_embeddings`: Chunks with vector embeddings (384 dim)
- `komite_audit_conversations`: Chat history
- `agent_logs`: Agent execution metrics

Uses `search_komite_audit_embeddings` stored procedure for vector similarity search.

## Agent Keys
When referencing agents in code: `charter_expert`, `planning_expert`, `financial_review_expert`, `regulatory_expert`, `banking_expert`, `reporting_expert`
