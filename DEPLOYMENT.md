# Deployment Guide - RAG Komite Audit System

Panduan lengkap untuk deploy aplikasi RAG Komite Audit ke production.

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Deployment Platforms](#deployment-platforms)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Local Development

### Quick Start

**Linux/Mac:**
```bash
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

**Windows:**
```cmd
setup.bat
start.bat
```

### Manual Start

**Backend:**
```bash
python -m backend.main
# Runs on http://localhost:8000
```

**Frontend:**
```bash
streamlit run frontend/app.py
# Opens automatically in browser
```

---

## 🚀 Production Deployment

### Option 1: Monolithic Deployment (Recommended for Small Scale)

Deploy backend dan frontend dalam satu server.

#### Railway (Recommended)

1. **Prepare for Deployment**

Create `Procfile`:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:
```
python-3.10.x
```

2. **Deploy to Railway**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables in Railway dashboard
# Set PORT=8000

# Deploy
railway up
```

3. **Configure Domain**
- Go to Railway dashboard
- Settings > Generate Domain
- Add custom domain (optional)

#### Render

1. **Create `render.yaml`**

```yaml
services:
  - type: web
    name: rag-komite-audit
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: GROQ_API_KEY
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: SUPABASE_SERVICE_KEY
        sync: false
```

2. **Deploy**
- Connect GitHub repository to Render
- Render will auto-deploy on push

### Option 2: Microservices Deployment (Scalable)

Deploy backend dan frontend secara terpisah.

#### Backend to Fly.io

1. **Install Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Create `fly.toml`**
```toml
app = "rag-komite-audit-backend"

[build]
  builder = "paketobuildpacks/builder:base"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[env]
  PORT = "8000"
```

3. **Deploy**
```bash
fly launch
fly secrets set GROQ_API_KEY=your_key
fly secrets set SUPABASE_URL=your_url
fly secrets set SUPABASE_KEY=your_key
fly secrets set SUPABASE_SERVICE_KEY=your_key
fly deploy
```

#### Frontend to Streamlit Cloud

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy to Streamlit Cloud**
- Go to https://share.streamlit.io
- Connect GitHub repository
- Select `frontend/app.py` as main file
- Add secrets in dashboard:
  ```toml
  API_BASE_URL = "https://your-backend-url.fly.dev"
  ```

### Option 3: Docker Deployment

#### Create Dockerfile for Backend

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - API_BASE_URL=http://backend:8000
    restart: unless-stopped
```

#### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## ⚙️ Environment Configuration

### Production .env

```env
# Groq API
GROQ_API_KEY=your_production_key
GROQ_MODEL=llama-3.1-70b-versatile

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key

# App Config
ENVIRONMENT=production
LOG_LEVEL=WARNING
APP_NAME=RAG Komite Audit System
APP_VERSION=1.0.0

# Vector Store
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DIMENSION=384
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Agent Config
MAX_AGENT_ITERATIONS=3
AGENT_TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Security Best Practices

1. **Never commit secrets to Git**
```bash
# Add to .gitignore
.env
*.env
.env.*
!.env.example
```

2. **Use Environment Variables**
- Railway: Use dashboard to set environment variables
- Render: Use environment variables in dashboard
- Fly.io: Use `fly secrets set KEY=value`
- Docker: Use `.env` file with docker-compose

3. **Secure API Keys**
- Use different keys for development and production
- Rotate keys regularly
- Monitor API usage

---

## 📊 Monitoring & Maintenance

### Logging

**Backend Logs:**
```bash
# Local
tail -f logs/backend.log

# Railway
railway logs

# Render
View in dashboard

# Fly.io
fly logs
```

**Frontend Logs:**
- Streamlit Cloud: View in dashboard
- Docker: `docker-compose logs frontend`

### Health Checks

Add health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "llm": "connected"
    }
```

### Database Maintenance

**Supabase:**
1. Regular backups (automatic in paid plans)
2. Monitor database size
3. Optimize indexes
4. Clean up old conversations:

```sql
-- Delete conversations older than 30 days
DELETE FROM komite_audit_conversations 
WHERE created_at < NOW() - INTERVAL '30 days';

-- Vacuum to reclaim space
VACUUM ANALYZE;
```

### Performance Monitoring

**Metrics to Monitor:**
- API response times
- Database query performance
- Vector search latency
- LLM API usage
- Memory usage
- CPU usage

**Tools:**
- Railway/Render/Fly.io: Built-in metrics
- Supabase: Database insights
- Groq: API usage dashboard

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend Won't Start

**Error: "Module not found"**
```bash
pip install -r requirements.txt --force-reinstall
```

**Error: "Cannot connect to database"**
- Check SUPABASE_URL and keys in environment variables
- Verify Supabase project is active
- Check network connectivity

#### 2. Frontend Can't Connect to Backend

**Check API_BASE_URL:**
```python
# In frontend/app.py
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

**CORS Issues:**
- Ensure backend allows frontend origin
- Add to FastAPI CORS middleware:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. Document Processing Fails

**Large Files:**
- Increase timeout in deployment platform
- Process in background
- Consider file size limits

**Encoding Issues:**
```python
# In document_processor.py
text = file.read().decode('utf-8', errors='ignore')
```

#### 4. Slow Responses

**Optimize:**
- Reduce `top_k` in similarity search
- Reduce `max_agents`
- Increase `match_threshold`
- Cache frequently accessed data

#### 5. Memory Issues

**Solutions:**
- Upgrade to larger instance
- Implement pagination
- Clean up old data
- Optimize chunking strategy

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        # Add your tests here
        python -m pytest tests/
    
    - name: Deploy to Railway
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      run: |
        npm install -g @railway/cli
        railway up
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Deploy multiple backend instances behind load balancer
- Use Redis for session management
- Implement rate limiting

### Database Scaling
- Upgrade Supabase plan for more connections
- Implement connection pooling
- Add read replicas for heavy read workloads

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_embedding(text: str):
    return embedding_manager.generate_embedding(text)
```

---

## 🎯 Production Checklist

- [ ] All secrets configured in environment variables
- [ ] Database schema deployed to Supabase
- [ ] Health check endpoint working
- [ ] Logging configured properly
- [ ] CORS configured correctly
- [ ] SSL/TLS enabled (HTTPS)
- [ ] Rate limiting implemented
- [ ] Error handling comprehensive
- [ ] Backup strategy in place
- [ ] Monitoring set up
- [ ] Documentation updated
- [ ] Load testing performed

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud)
- [Supabase Documentation](https://supabase.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Fly.io Documentation](https://fly.io/docs/)

---

**Last Updated:** January 2026
