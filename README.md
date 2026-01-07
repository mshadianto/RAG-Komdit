# RAG Agentic AI - Komite Audit System

**Multi-Agent RAG System untuk Expertise Komite Audit Indonesia**

Sistem AI canggih yang menggunakan arsitektur multi-agent untuk menjawab pertanyaan seputar Komite Audit, governance, audit planning, regulasi, dan compliance. Menggunakan dokumen Anda sendiri sebagai knowledge base dengan teknologi RAG (Retrieval Augmented Generation).

---

## 🎯 Fitur Utama

### Multi-Agent Architecture
6 Expert Agents yang specialized:

1. **Audit Committee Charter Expert**
   - Penyusunan Audit Committee Charter
   - Internal Audit Charter
   - Best practices governance
   - Hubungan Komite Audit dengan Board

2. **Audit Planning & Execution Expert**
   - Audit planning process
   - Risk assessment
   - Review kinerja fungsi audit intern

3. **Financial Reporting Review Expert**
   - Review laporan keuangan
   - Efektivitas akuntan publik
   - Proses penunjukan auditor eksternal

4. **Regulatory Compliance Expert**
   - UU Pasar Modal
   - PSAK (Pernyataan Standar Akuntansi Keuangan)
   - SPAP (Standar Profesional Akuntan Publik)
   - OJK regulations

5. **Banking Audit Committee Expert**
   - Peraturan BI/OJK untuk perbankan
   - Peran Komite Audit di bank
   - Risk management banking

6. **Reporting & Disclosure Expert**
   - Penyusunan laporan periodik
   - Disclosure dalam annual report
   - Communication dengan stakeholders

### RAG (Retrieval Augmented Generation)
- Upload dokumen Anda sendiri (PDF, DOCX, TXT, XLSX)
- Automatic chunking dan embedding
- Semantic search dengan pgvector
- Context-aware responses

### Intelligent Query Routing
- Automatic routing ke expert agent yang tepat
- Multi-agent collaboration untuk pertanyaan kompleks
- Response synthesis dari multiple agents

---

## 🛠️ Teknologi Stack

### Free Tier Tools:
- **LLM**: Groq API (Llama 3.1 70B) - Free tier
- **Vector Store**: Supabase + pgvector - Free tier
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2) - Open source
- **Backend**: FastAPI + Python 3.10+
- **Frontend**: Streamlit
- **Database**: PostgreSQL with pgvector extension

---

## 📋 Prerequisites

- Python 3.10 or higher
- Groq API Key (free dari https://console.groq.com)
- Supabase Account (free dari https://supabase.com)
- Git

---

## 🚀 Setup & Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd rag-komite-audit
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Supabase Database

1. Buat project baru di [Supabase](https://supabase.com)
2. Buka SQL Editor
3. Copy dan jalankan script dari `config/database_schema.sql`
4. Catat URL dan API keys dari Project Settings > API

### 5. Setup Environment Variables

```bash
# Copy .env.example ke .env
cp .env.example .env
```

Edit `.env` file dengan credentials Anda:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
```

### 6. Download Embedding Model

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

---

## 🎮 Running the Application

### Start Backend Server

```bash
cd rag-komite-audit
python -m backend.main
```

Backend akan berjalan di `http://localhost:8000`

### Start Frontend

Buka terminal baru:

```bash
cd rag-komite-audit
streamlit run frontend/app.py
```

Frontend akan terbuka otomatis di browser Anda.

---

## 📖 Cara Penggunaan

### 1. Upload Documents

1. Buka menu "Documents" di sidebar
2. Upload dokumen (PDF, DOCX, TXT, XLSX)
3. Sistem akan otomatis:
   - Extract text
   - Detect category
   - Generate tags
   - Chunk dan embed text
   - Store di vector database

### 2. Chat dengan Expert Agents

1. Buka menu "Chat"
2. Tulis pertanyaan Anda tentang Komite Audit
3. Sistem akan:
   - Route query ke expert agent yang tepat
   - Retrieve relevant context dari dokumen
   - Generate comprehensive response
   - Synthesize jika menggunakan multiple agents

### 3. Monitor Analytics

1. Buka menu "Analytics"
2. Lihat statistics:
   - Document distribution by category
   - Agent performance metrics
   - Success rates
   - Processing times

---

## 📁 Struktur Project

```
rag-komite-audit/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database operations
│   ├── embeddings.py        # Embedding management
│   ├── llm_client.py        # Groq API client
│   └── document_processor.py # Document processing
├── agents/
│   └── orchestrator.py      # Multi-agent orchestration
├── frontend/
│   └── app.py               # Streamlit application
├── config/
│   ├── config.py            # Configuration management
│   └── database_schema.sql  # Database schema
├── data/
│   ├── uploads/             # Uploaded documents
│   └── processed/           # Processed documents
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔑 API Endpoints

### Query Endpoint
```http
POST /query
Content-Type: application/json

{
  "query": "Jelaskan peran Komite Audit dalam audit planning",
  "session_id": "unique-session-id",
  "use_context": true,
  "max_agents": 2
}
```

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

file: [binary]
category: "Audit Planning" (optional)
```

### List Documents
```http
GET /documents?category=Banking&status=processed&limit=50
```

### Get Statistics
```http
GET /statistics/documents
GET /statistics/agents
```

---

## 🎓 Best Practices

### Document Upload
- Upload dokumen yang relevan dengan topik Komite Audit
- Pastikan dokumen memiliki struktur yang jelas
- PDF dengan text yang searchable (bukan scan image)
- File size maksimal yang reasonable (< 50MB per file)

### Query Tips
- Buat pertanyaan yang spesifik
- Gunakan bahasa Indonesia atau English
- Sebutkan konteks jika diperlukan
- Contoh baik: "Bagaimana proses penunjukan auditor eksternal sesuai regulasi OJK?"
- Contoh kurang baik: "Audit?"

### Context Usage
- Enable "Use Document Context" untuk pertanyaan yang memerlukan informasi dari dokumen
- Disable jika ingin jawaban general knowledge saja
- Max agents: 2-3 untuk hasil optimal

---

## 🔧 Troubleshooting

### Error: "Cannot connect to database"
- Pastikan Supabase credentials benar di `.env`
- Check internet connection
- Verify Supabase project is active

### Error: "Model not found"
- Run: `pip install sentence-transformers`
- Download model: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"`

### Error: "Groq API rate limit"
- Groq free tier memiliki rate limit
- Tunggu beberapa menit
- Consider upgrade ke paid tier jika perlu throughput tinggi

### Documents not processing
- Check file format (harus PDF, DOCX, TXT, atau XLSX)
- Check file size (< 50MB recommended)
- Check backend logs untuk error details

---

## 🚀 Production Deployment

### Recommended Services:
- **Backend**: Railway, Render, atau Fly.io
- **Frontend**: Streamlit Community Cloud
- **Database**: Supabase (production plan)
- **LLM**: Groq API atau self-hosted

### Environment Variables for Production:
```env
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

### Security Considerations:
- Use HTTPS for all connections
- Keep API keys secure (never commit to git)
- Enable CORS only for trusted domains
- Use rate limiting for API endpoints
- Regular backup of Supabase database

---

## 📊 Performance Optimization

### Vector Search
- Adjust `match_threshold` (default: 0.7) untuk precision vs recall
- Adjust `top_k` (default: 5) untuk jumlah context

### Chunking
- `CHUNK_SIZE=500` (adjustable untuk dokumen yang panjang/pendek)
- `CHUNK_OVERLAP=50` untuk semantic continuity

### LLM
- `AGENT_TEMPERATURE=0.7` untuk balance creativity vs consistency
- `MAX_TOKENS=2000` untuk response length

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💼 Developer

**MS Hadianto, SE, Ak, M.M., CACP®, CCFA®, QIA®, CA®, GRCP®, GRCA®, CGP®**

- Audit Committee Member at BPKH
- EmESHa Consulting
- HADIANT Platform
- GitHub: mshadianto

---

## 📞 Support

For issues and questions:
- Open GitHub Issue
- Contact developer
- Check documentation

---

## 🎉 Acknowledgments

- Groq for free LLM API
- Supabase for free database hosting
- Sentence Transformers for open-source embeddings
- FastAPI and Streamlit communities

---

**Version:** 1.0.0  
**Last Updated:** January 2026
