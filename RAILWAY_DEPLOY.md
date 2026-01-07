# Railway Deployment Guide

Deploy backend dan frontend ke Railway dari satu repository.

## Step 1: Setup Project

1. Login ke [railway.app](https://railway.app) dengan GitHub
2. **New Project** → **Deploy from GitHub repo** → pilih `RAG-Komdit`

## Step 2: Deploy Backend

Service pertama akan otomatis dibuat. Konfigurasi:

- **Name**: `backend` (atau biarkan default)
- **Start Command**: (otomatis dari nixpacks.toml)
  ```
  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
  ```

### Environment Variables (Backend)
```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-70b-versatile
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

Catat URL backend setelah deploy (contoh: `https://backend-xxx.railway.app`)

## Step 3: Deploy Frontend

1. Di project yang sama, klik **New** → **Service** → **GitHub Repo**
2. Pilih repository `RAG-Komdit` yang sama
3. Buka **Settings** → ubah:
   - **Service Name**: `frontend`
   - **Start Command**:
     ```
     streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
     ```

### Environment Variables (Frontend)
```
API_BASE_URL=https://backend-xxx.railway.app
```
(Ganti dengan URL backend dari Step 2)

## Step 4: Generate Domain

Untuk setiap service:
1. Buka **Settings** → **Networking**
2. Klik **Generate Domain**

## URLs

Setelah deploy:
- **Backend API**: `https://backend-xxx.railway.app`
- **Frontend App**: `https://frontend-xxx.railway.app`

## Troubleshooting

### Build Error
- Pastikan Python 3.10+ terinstall
- Cek logs di Railway dashboard

### Connection Error
- Pastikan `API_BASE_URL` di frontend sudah benar
- Cek backend sudah running dengan akses `/health` endpoint

### Database Error
- Pastikan Supabase credentials benar
- Cek Supabase project aktif dan schema sudah dijalankan
