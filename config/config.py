"""
Configuration Management for RAG Komite Audit System
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # Groq Configuration
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # Vector Store Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_DIMENSION: int = 384
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # Application Configuration
    APP_NAME: str = "RAG Komite Audit System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Agent Configuration
    MAX_AGENT_ITERATIONS: int = 3
    AGENT_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # Database Tables
    DOCUMENTS_TABLE: str = "komite_audit_documents"
    EMBEDDINGS_TABLE: str = "komite_audit_embeddings"
    CONVERSATIONS_TABLE: str = "komite_audit_conversations"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Initialize settings
settings = Settings()

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"

# Create directories if they don't exist
for directory in [DATA_DIR, UPLOAD_DIR, PROCESSED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Agent definitions
AGENT_ROLES = {
    "charter_expert": {
        "name": "Audit Committee Charter Expert",
        "description": "Expert dalam penyusunan Audit Committee Charter dan Internal Audit Charter",
        "expertise": [
            "Struktur dan isi Audit Committee Charter",
            "Internal Audit Charter",
            "Best practices governance",
            "Hubungan Komite Audit dengan Board dan Management"
        ]
    },
    "planning_expert": {
        "name": "Audit Planning & Execution Expert",
        "description": "Expert dalam perencanaan dan pelaksanaan audit",
        "expertise": [
            "Audit planning process",
            "Risk assessment",
            "Audit program development",
            "Review kinerja fungsi audit intern"
        ]
    },
    "financial_review_expert": {
        "name": "Financial Reporting Review Expert",
        "description": "Expert dalam review laporan keuangan dan efektivitas akuntan publik",
        "expertise": [
            "Review laporan keuangan",
            "Efektivitas dan objektivitas akuntan publik",
            "Proses penunjukan auditor eksternal",
            "Quality control audit eksternal"
        ]
    },
    "regulatory_expert": {
        "name": "Regulatory Compliance Expert",
        "description": "Expert dalam peraturan dan standar terkait Komite Audit",
        "expertise": [
            "UU Pasar Modal",
            "PSAK (Pernyataan Standar Akuntansi Keuangan)",
            "SPAP (Standar Profesional Akuntan Publik)",
            "OJK regulations",
            "Standarisasi Komite Audit"
        ]
    },
    "banking_expert": {
        "name": "Banking Audit Committee Expert",
        "description": "Expert khusus Komite Audit di sektor perbankan",
        "expertise": [
            "Peraturan BI/OJK untuk perbankan",
            "Peran Komite Audit di bank",
            "Risk management banking",
            "Compliance banking sector"
        ]
    },
    "reporting_expert": {
        "name": "Reporting & Disclosure Expert",
        "description": "Expert dalam pelaporan dan pengungkapan kegiatan Komite Audit",
        "expertise": [
            "Penyusunan laporan periodik",
            "Disclosure dalam annual report",
            "Communication dengan stakeholders",
            "Transparency dan accountability"
        ]
    }
}

# System prompts for agents
SYSTEM_PROMPTS = {
    "query_router": """Anda adalah Query Router Agent yang ahli dalam menganalisis pertanyaan tentang Komite Audit dan mengarahkannya ke expert agent yang tepat.

Expert agents yang tersedia:
1. charter_expert - Untuk pertanyaan tentang Audit Committee Charter dan Internal Audit Charter
2. planning_expert - Untuk pertanyaan tentang audit planning dan execution
3. financial_review_expert - Untuk pertanyaan tentang review laporan keuangan dan akuntan publik
4. regulatory_expert - Untuk pertanyaan tentang regulasi (UU Pasar Modal, PSAK, SPAP)
5. banking_expert - Untuk pertanyaan khusus Komite Audit di perbankan
6. reporting_expert - Untuk pertanyaan tentang pelaporan dan disclosure

Analisis pertanyaan user dan tentukan expert agent yang paling sesuai. Jika pertanyaan kompleks dan memerlukan multiple experts, tentukan urutan prioritasnya.

Berikan output dalam format JSON:
{
    "primary_agent": "agent_key",
    "secondary_agents": ["agent_key1", "agent_key2"],
    "reasoning": "penjelasan singkat"
}""",
    
    "synthesizer": """Anda adalah Synthesizer Agent yang bertugas menggabungkan insights dari multiple expert agents menjadi jawaban komprehensif dan koheren.

Tugas Anda:
1. Mengintegrasikan informasi dari berbagai expert agents
2. Menghilangkan duplikasi dan kontradiksi
3. Menyusun jawaban yang terstruktur dan mudah dipahami
4. Memberikan referensi ke dokumen sumber jika ada
5. Menambahkan insights tambahan jika relevan

Format jawaban:
- Gunakan struktur yang jelas dengan paragraf
- Gunakan bullet points hanya jika diperlukan untuk clarity
- Sertakan referensi/citation jika ada
- Tambahkan disclaimer jika diperlukan""",
}
