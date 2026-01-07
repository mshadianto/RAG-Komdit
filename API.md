# API Documentation

Dokumentasi lengkap REST API endpoints untuk RAG Komite Audit System.

**Base URL:** `http://localhost:8000` (development) atau `https://your-domain.com` (production)

---

## Authentication

Saat ini API tidak menggunakan authentication. Untuk production, disarankan menambahkan:
- API Key authentication
- JWT tokens
- OAuth 2.0

---

## Endpoints

### Health Check

#### GET /health
Check system health status

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "llm_model": "llama-3.1-70b-versatile",
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

---

### Query Processing

#### POST /query
Process user query through multi-agent system

**Request Body:**
```json
{
  "query": "Jelaskan peran Komite Audit dalam audit planning",
  "session_id": "unique-session-id",
  "use_context": true,
  "max_agents": 2
}
```

**Parameters:**
- `query` (string, required): User's question
- `session_id` (string, required): Unique session identifier
- `use_context` (boolean, optional): Whether to use document context (default: true)
- `max_agents` (integer, optional): Maximum agents to use (1-3, default: 2)

**Response:**
```json
{
  "success": true,
  "response": "Komite Audit memiliki peran penting dalam audit planning...",
  "agents_used": ["Audit Planning & Execution Expert"],
  "routing_reasoning": "Query tentang audit planning",
  "context_count": 3,
  "processing_time_ms": 2453,
  "conversation_id": "uuid-here",
  "metadata": {
    "document_ids": ["doc-id-1", "doc-id-2"],
    "similarity_scores": [0.89, 0.76, 0.72]
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "response": "Error message",
  "error": "Detailed error"
}
```

---

### Document Management

#### POST /upload
Upload and process document

**Request:**
- Content-Type: `multipart/form-data`
- Form fields:
  - `file`: File to upload (PDF, DOCX, TXT, XLSX)
  - `category` (optional): Document category

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf" \
  -F "category=Audit Planning"
```

**Response:**
```json
{
  "success": true,
  "message": "Document uploaded successfully. Processing in background.",
  "filename": "document.pdf",
  "file_size": 245678
}
```

#### GET /documents
List all documents with optional filters

**Query Parameters:**
- `category` (string, optional): Filter by category
- `status` (string, optional): Filter by status (uploaded, processing, processed, error)
- `limit` (integer, optional): Maximum number of results (default: 100)

**Example:**
```bash
curl "http://localhost:8000/documents?category=Banking&status=processed&limit=50"
```

**Response:**
```json
{
  "documents": [
    {
      "id": "uuid",
      "filename": "banking-audit.pdf",
      "file_type": "PDF Document",
      "file_size": 245678,
      "category": "Banking",
      "tags": ["audit", "banking", "compliance"],
      "status": "processed",
      "total_chunks": 45,
      "upload_date": "2026-01-06T10:30:00Z",
      "processed_date": "2026-01-06T10:31:25Z"
    }
  ]
}
```

#### GET /documents/{document_id}
Get document details by ID

**Response:**
```json
{
  "id": "uuid",
  "filename": "document.pdf",
  "file_type": "PDF Document",
  "file_size": 245678,
  "category": "Audit Planning",
  "tags": ["audit", "planning"],
  "status": "processed",
  "total_chunks": 32,
  "upload_date": "2026-01-06T10:30:00Z",
  "processed_date": "2026-01-06T10:31:25Z",
  "metadata": {}
}
```

#### DELETE /documents/{document_id}
Delete document and its embeddings

**Response:**
```json
{
  "success": true,
  "message": "Document deleted successfully",
  "document_id": "uuid"
}
```

---

### Conversation History

#### GET /conversations/{session_id}
Get conversation history for a session

**Query Parameters:**
- `limit` (integer, optional): Maximum number of conversations (default: 10)

**Response:**
```json
{
  "history": [
    {
      "id": "uuid",
      "session_id": "session-123",
      "user_query": "What is audit committee?",
      "agent_response": "Komite Audit adalah...",
      "agents_used": ["Audit Committee Charter Expert"],
      "context_documents": ["doc-id-1"],
      "similarity_scores": [0.89],
      "processing_time_ms": 2450,
      "created_at": "2026-01-06T10:30:00Z"
    }
  ]
}
```

---

### Feedback

#### POST /feedback
Submit feedback for a conversation

**Request Body:**
```json
{
  "conversation_id": "uuid",
  "rating": 5,
  "comment": "Very helpful response"
}
```

**Parameters:**
- `conversation_id` (string, required): Conversation ID
- `rating` (integer, required): Rating 1-5
- `comment` (string, optional): Additional feedback

**Response:**
```json
{
  "success": true,
  "message": "Feedback submitted successfully"
}
```

---

### Statistics

#### GET /statistics/documents
Get document statistics by category

**Response:**
```json
{
  "statistics": [
    {
      "category": "Audit Planning",
      "total_documents": 15,
      "total_chunks": 450,
      "avg_file_size": 125678,
      "last_upload": "2026-01-06T10:30:00Z"
    }
  ]
}
```

#### GET /statistics/agents
Get agent performance metrics

**Response:**
```json
{
  "statistics": [
    {
      "agent_name": "Audit Planning & Execution Expert",
      "agent_role": "planning_expert",
      "total_executions": 150,
      "avg_execution_time": 2345,
      "avg_tokens_used": 850,
      "success_rate": 0.98
    }
  ]
}
```

---

### Agent Information

#### GET /agents
List available expert agents

**Response:**
```json
{
  "agents": {
    "charter_expert": {
      "name": "Audit Committee Charter Expert",
      "description": "Expert dalam penyusunan Audit Committee Charter",
      "expertise": [
        "Struktur dan isi Audit Committee Charter",
        "Internal Audit Charter",
        "Best practices governance"
      ]
    }
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production:

**Recommended Limits:**
- Query endpoint: 100 requests/hour per IP
- Upload endpoint: 20 uploads/hour per IP
- Other endpoints: 1000 requests/hour per IP

---

## WebSocket Support (Future)

Future versions may include WebSocket support for:
- Real-time query streaming
- Live document processing updates
- Agent execution progress

---

## Examples

### Python Client Example

```python
import requests

# Query example
def query_agent(question: str, session_id: str):
    response = requests.post(
        "http://localhost:8000/query",
        json={
            "query": question,
            "session_id": session_id,
            "use_context": True,
            "max_agents": 2
        }
    )
    return response.json()

# Upload example
def upload_document(file_path: str, category: str = None):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'category': category} if category else {}
        response = requests.post(
            "http://localhost:8000/upload",
            files=files,
            data=data
        )
    return response.json()

# Usage
result = query_agent("Apa peran Komite Audit?", "session-123")
print(result['response'])

upload_result = upload_document("document.pdf", "Audit Planning")
print(upload_result['message'])
```

### JavaScript Client Example

```javascript
// Query example
async function queryAgent(question, sessionId) {
  const response = await fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: question,
      session_id: sessionId,
      use_context: true,
      max_agents: 2
    })
  });
  return await response.json();
}

// Upload example
async function uploadDocument(file, category) {
  const formData = new FormData();
  formData.append('file', file);
  if (category) formData.append('category', category);
  
  const response = await fetch('http://localhost:8000/upload', {
    method: 'POST',
    body: formData
  });
  return await response.json();
}

// Usage
const result = await queryAgent('Apa peran Komite Audit?', 'session-123');
console.log(result.response);
```

---

## OpenAPI Documentation

Interactive API documentation tersedia di:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

**Last Updated:** January 2026
