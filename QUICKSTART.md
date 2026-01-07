# Quick Start Guide

Panduan cepat untuk mulai menggunakan RAG Komite Audit System dalam 5 menit.

---

## 📦 Prerequisites

✅ Python 3.10+ terinstall  
✅ Git terinstall  
✅ Akun Groq (free) - https://console.groq.com  
✅ Akun Supabase (free) - https://supabase.com  

---

## 🚀 5-Minute Setup

### Step 1: Clone Repository (1 min)

```bash
git clone <your-repo-url>
cd rag-komite-audit
```

### Step 2: Run Setup Script (2 min)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

Script akan:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Download embedding model
- ✅ Create .env file

### Step 3: Configure Credentials (1 min)

Edit `.env` file:

```env
GROQ_API_KEY=your_groq_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
```

**Get Groq API Key:**
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy and paste to .env

**Get Supabase Keys:**
1. Go to https://supabase.com
2. Create new project
3. Go to Settings > API
4. Copy URL and keys to .env

### Step 4: Setup Database (1 min)

1. Open Supabase SQL Editor
2. Copy content from `config/database_schema.sql`
3. Paste and run
4. Wait for completion

### Step 5: Start Application (10 seconds)

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Manual start:**
```bash
# Terminal 1 - Backend
python -m backend.main

# Terminal 2 - Frontend
streamlit run frontend/app.py
```

Application will open in browser automatically! 🎉

---

## 📝 First Steps

### 1. Upload Your First Document

1. Click "Documents" in sidebar
2. Click "Upload Document"
3. Select a PDF/DOCX about Komite Audit
4. Wait for processing (background task)
5. Document will appear in list when ready

**Don't have documents?** Use sample questions below without uploading documents first. The system can still answer based on general knowledge.

### 2. Ask Your First Question

1. Click "Chat" in sidebar
2. Enter question, for example:
   ```
   Apa peran utama Komite Audit dalam proses audit?
   ```
3. Click "Submit"
4. See which expert agent answered
5. View processing time and context used

### 3. Try Different Questions

**Charter & Governance:**
```
Jelaskan struktur Audit Committee Charter yang efektif
```

**Audit Planning:**
```
Bagaimana Komite Audit berperan dalam audit planning?
```

**Financial Review:**
```
Apa yang harus direview Komite Audit dalam laporan keuangan?
```

**Regulatory:**
```
Apa peraturan OJK terkait Komite Audit?
```

**Banking:**
```
Bagaimana tugas Komite Audit di bank berbeda dengan perusahaan lain?
```

### 4. Check Analytics

1. Click "Analytics" in sidebar
2. See document statistics
3. See agent performance
4. Monitor system usage

---

## 🎯 Sample Scenarios

### Scenario 1: Research Regulation

**Goal:** Understand OJK regulations about audit committee

**Steps:**
1. Upload OJK regulation documents
2. Ask: "Apa persyaratan OJK untuk anggota Komite Audit?"
3. System will search documents and provide accurate answer
4. Click document links to see sources

### Scenario 2: Prepare Charter

**Goal:** Create audit committee charter

**Steps:**
1. Upload sample charters from other companies
2. Ask: "Buatkan draft Audit Committee Charter untuk perusahaan properti"
3. System will use charter expert + your documents
4. Get customized charter draft

### Scenario 3: Review Process

**Goal:** Understand review process for financial statements

**Steps:**
1. Upload internal audit manual
2. Ask: "Bagaimana Komite Audit melakukan review laporan keuangan?"
3. System combines documents + expert knowledge
4. Get step-by-step process

---

## ⚙️ Configuration Tips

### For Better Results

**Enable Context Search:**
```python
use_context = True  # Always use for specific questions
```

**Adjust Agents:**
```python
max_agents = 2  # Balance between speed and depth
# 1 = Fast, focused
# 2 = Balanced (recommended)
# 3 = Comprehensive, slower
```

**Similarity Threshold:**
Edit `config/config.py`:
```python
VECTOR_SIMILARITY_THRESHOLD = 0.7  # Default
# Lower (0.5-0.6) = More results, less precise
# Higher (0.8-0.9) = Fewer results, more precise
```

### For Production

1. Set environment to production:
```env
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

2. Enable HTTPS
3. Add authentication
4. Set up monitoring
5. Configure backups

See `DEPLOYMENT.md` for details.

---

## 🐛 Common Issues

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Cannot connect to Supabase"
**Solution:**
- Check .env file has correct credentials
- Verify Supabase project is active
- Test connection: `curl https://your-project.supabase.co`

### Issue: "Groq API error"
**Solution:**
- Check API key is valid
- Check rate limits (free tier: limited requests)
- Wait a few minutes if rate limited

### Issue: "Port already in use"
**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn backend.main:app --port 8001
```

---

## 📚 Next Steps

After setup:

1. **Read Full Documentation**
   - README.md - Complete features
   - API.md - API documentation
   - DEPLOYMENT.md - Production deployment

2. **Customize Agents**
   - Edit `config/config.py`
   - Modify agent prompts
   - Add new expert agents

3. **Upload Documents**
   - Add your organization's documents
   - Internal audit manuals
   - Policies and procedures
   - Regulatory documents

4. **Integrate**
   - Use REST API in your apps
   - Build custom frontend
   - Integrate with existing systems

---

## 🆘 Get Help

- 📖 Check documentation in `/docs`
- 🐛 Open GitHub issue
- 💬 Contact developer
- 📧 Email support

---

## ✅ Checklist

Setup completed when you can:

- [ ] Access frontend at http://localhost:8501
- [ ] Access backend at http://localhost:8000
- [ ] Upload a document successfully
- [ ] Ask a question and get answer
- [ ] See conversation in history
- [ ] View analytics dashboard

**Congratulations! You're ready to use RAG Komite Audit System! 🎉**

---

**Time to Complete:** ~5 minutes  
**Difficulty:** Easy  
**Last Updated:** January 2026
