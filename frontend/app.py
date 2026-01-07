"""
Streamlit Frontend for RAG Komite Audit System
Professional minimalist interface - McKinsey style
"""
import streamlit as st
import requests
import uuid
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import os

# Page configuration
st.set_page_config(
    page_title="Komite Audit Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# App Version
APP_VERSION = "1.0.0"

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'prefilled_query' not in st.session_state:
    st.session_state.prefilled_query = ""

# McKinsey-style Professional CSS with Landing Page Enhancements
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Color Variables - McKinsey Navy Theme */
    :root {
        --primary-navy: #003366;
        --secondary-navy: #0a4d8c;
        --accent-teal: #0097a7;
        --light-gray: #f5f7fa;
        --medium-gray: #e8eaed;
        --dark-gray: #5f6368;
        --text-primary: #1a1a2e;
        --text-secondary: #5f6368;
        --white: #ffffff;
        --success: #0d7377;
        --border: #e0e0e0;
    }

    /* ===== LANDING PAGE STYLES ===== */

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #003366 0%, #0a4d8c 50%, #0097a7 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
        font-weight: 400;
    }

    .hero-description {
        font-size: 1rem;
        opacity: 0.8;
        max-width: 700px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* Agent Cards for Landing */
    .agent-card-landing {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        cursor: default;
    }

    .agent-card-landing:hover {
        box-shadow: 0 8px 25px rgba(0,51,102,0.15);
        transform: translateY(-2px);
        border-color: #0097a7;
    }

    .agent-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .agent-card-landing h4 {
        color: #003366;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .agent-card-landing p {
        color: #5f6368;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 0.75rem;
    }

    .agent-card-landing ul {
        margin: 0;
        padding-left: 1.2rem;
        color: #5f6368;
        font-size: 0.8rem;
    }

    .agent-card-landing li {
        margin-bottom: 0.25rem;
    }

    /* How It Works Section */
    .how-it-works {
        background: #f5f7fa;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
    }

    .step-card {
        text-align: center;
        padding: 1.5rem 1rem;
    }

    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #003366 0%, #0097a7 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 1rem auto;
    }

    .step-title {
        color: #003366;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .step-desc {
        color: #5f6368;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* Example Query Cards */
    .example-query-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-left: 4px solid #0097a7;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .example-query-card:hover {
        background: #f5f7fa;
        border-left-color: #003366;
        box-shadow: 0 2px 8px rgba(0,51,102,0.1);
    }

    .example-query-card p {
        margin: 0;
        color: #1a1a2e;
        font-size: 0.9rem;
    }

    .example-query-card span {
        color: #0097a7;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Stats Cards */
    .stat-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
    }

    .stat-card:hover {
        box-shadow: 0 4px 12px rgba(0,51,102,0.1);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #003366;
        line-height: 1;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #5f6368;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }

    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Section Headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #003366;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #5f6368;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* ===== EXISTING STYLES ===== */

    /* Main Header */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: var(--primary-navy);
        text-align: left;
        padding: 0.5rem 0;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
    }

    .sub-header {
        font-size: 1rem;
        color: var(--text-secondary);
        text-align: left;
        padding-bottom: 1.5rem;
        font-weight: 400;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-navy);
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent-teal);
        display: inline-block;
    }

    /* Agent Cards */
    .agent-card {
        background-color: var(--white);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1.25rem;
        margin: 0.5rem 0;
        transition: box-shadow 0.2s ease;
    }

    .agent-card:hover {
        box-shadow: 0 2px 8px rgba(0,51,102,0.1);
    }

    .agent-card h4 {
        color: var(--primary-navy);
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .agent-card p {
        color: var(--text-secondary);
        font-size: 0.85rem;
        line-height: 1.5;
        margin: 0;
    }

    /* Query Box */
    .query-box {
        background-color: var(--light-gray);
        border-left: 3px solid var(--primary-navy);
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        border-radius: 0 4px 4px 0;
    }

    .query-box strong {
        color: var(--primary-navy);
        font-weight: 600;
    }

    .query-meta {
        color: var(--text-secondary);
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }

    /* Response Box */
    .response-box {
        background-color: var(--white);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent-teal);
        padding: 1.25rem;
        margin: 0.75rem 0 1.5rem 0;
        border-radius: 0 4px 4px 0;
        line-height: 1.7;
    }

    .response-box strong {
        color: var(--accent-teal);
        font-weight: 600;
    }

    /* Metric Cards */
    .metric-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1.5rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: var(--primary-navy);
    }

    .metric-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--primary-navy);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--white);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
    }

    /* Button Styling */
    .stButton > button {
        background-color: var(--primary-navy);
        color: var(--white);
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }

    .stButton > button:hover {
        background-color: var(--secondary-navy);
    }

    .stButton > button[kind="primary"] {
        background-color: var(--accent-teal);
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #007d87;
    }

    /* Document Card */
    .doc-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .doc-title {
        font-weight: 600;
        color: var(--primary-navy);
    }

    .doc-meta {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* Status Badges */
    .status-processed {
        background-color: #e6f4ea;
        color: #1e7e34;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status-processing {
        background-color: #fff3e0;
        color: #e65100;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status-error {
        background-color: #fce8e6;
        color: #c5221f;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, var(--primary-navy) 0%, var(--secondary-navy) 100%);
        color: var(--white);
        padding: 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
    }

    .info-box h3 {
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }

    .info-box p {
        margin: 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }

    /* Table Styling */
    .dataframe {
        border: none !important;
    }

    .dataframe th {
        background-color: var(--primary-navy) !important;
        color: var(--white) !important;
        font-weight: 500 !important;
    }

    .dataframe td {
        border-color: var(--border) !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: var(--primary-navy);
    }

    /* Footer Styling */
    .app-footer {
        background: linear-gradient(135deg, #003366 0%, #0a4d8c 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 3rem;
        text-align: center;
    }

    .footer-disclaimer {
        font-size: 0.8rem;
        opacity: 0.8;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto 1.5rem auto;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
    }

    .footer-developer {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }

    .footer-version {
        font-size: 0.75rem;
        opacity: 0.6;
    }

    .footer-divider {
        width: 60px;
        height: 2px;
        background: rgba(255,255,255,0.3);
        margin: 1rem auto;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def call_api(endpoint: str, method: str = "GET", timeout: int = 120, **kwargs):
    """Call API endpoint with timeout"""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=timeout, **kwargs)
        elif method == "POST":
            response = requests.post(url, timeout=timeout, **kwargs)
        elif method == "DELETE":
            response = requests.delete(url, timeout=timeout, **kwargs)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timeout. Server mungkin sedang sibuk, coba lagi.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Tidak dapat terhubung ke server. Periksa koneksi.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def format_bytes(size):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

# Agent data for landing page
AGENT_INFO = {
    "charter_expert": {
        "icon": "📜",
        "name": "Charter Expert",
        "title": "Audit Committee Charter",
        "desc": "Ahli penyusunan Audit Committee Charter dan Internal Audit Charter",
        "expertise": ["Struktur Charter", "Best Practices Governance", "Hubungan dengan Board"]
    },
    "planning_expert": {
        "icon": "📋",
        "name": "Planning Expert",
        "title": "Audit Planning & Execution",
        "desc": "Ahli perencanaan dan pelaksanaan audit",
        "expertise": ["Risk Assessment", "Audit Program", "Review Kinerja Audit"]
    },
    "financial_review_expert": {
        "icon": "💰",
        "name": "Financial Review Expert",
        "title": "Financial Reporting Review",
        "desc": "Ahli review laporan keuangan dan efektivitas akuntan publik",
        "expertise": ["Review Laporan Keuangan", "Penunjukan Auditor", "Quality Control"]
    },
    "regulatory_expert": {
        "icon": "⚖️",
        "name": "Regulatory Expert",
        "title": "Regulatory Compliance",
        "desc": "Ahli peraturan dan standar terkait Komite Audit",
        "expertise": ["UU Pasar Modal", "PSAK & SPAP", "Regulasi OJK"]
    },
    "banking_expert": {
        "icon": "🏦",
        "name": "Banking Expert",
        "title": "Banking Audit Committee",
        "desc": "Ahli khusus Komite Audit di sektor perbankan",
        "expertise": ["Peraturan BI/OJK", "Risk Management", "Compliance Banking"]
    },
    "reporting_expert": {
        "icon": "📊",
        "name": "Reporting Expert",
        "title": "Reporting & Disclosure",
        "desc": "Ahli pelaporan dan pengungkapan kegiatan Komite Audit",
        "expertise": ["Laporan Periodik", "Annual Report Disclosure", "Stakeholder Communication"]
    }
}

EXAMPLE_QUERIES = [
    {"query": "Apa saja tugas dan tanggung jawab utama Komite Audit?", "agent": "Charter Expert"},
    {"query": "Bagaimana proses penunjukan auditor eksternal yang sesuai regulasi?", "agent": "Financial Review Expert"},
    {"query": "Apa saja peraturan OJK yang mengatur tentang Komite Audit?", "agent": "Regulatory Expert"},
    {"query": "Bagaimana peran Komite Audit dalam risk assessment?", "agent": "Planning Expert"},
    {"query": "Apa perbedaan Komite Audit di perbankan dengan sektor lain?", "agent": "Banking Expert"},
    {"query": "Bagaimana format disclosure Komite Audit dalam annual report?", "agent": "Reporting Expert"},
]

# Sidebar
with st.sidebar:
    # Logo and Title
    st.markdown("""
    <div style="padding: 1.5rem 1rem; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #0097a7 0%, #00bcd4 100%); border-radius: 12px; margin: 0 auto 0.75rem auto; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 1.5rem; font-weight: 700;">KA</span>
        </div>
        <h3 style="color: white; font-weight: 600; margin: 0; font-size: 1.1rem;">Komite Audit</h3>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.7rem; margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 1px;">Intelligence System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["Beranda", "Konsultasi", "Dokumen", "Analitik", "Tentang"],
        icons=["house-door", "chat-left-text", "folder2-open", "graph-up-arrow", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#0097a7", "font-size": "1rem"},
            "nav-link": {
                "font-size": "0.85rem",
                "text-align": "left",
                "margin": "0.15rem 0.5rem",
                "padding": "0.7rem 1rem",
                "color": "rgba(255,255,255,0.7)",
                "border-radius": "8px",
                "transition": "all 0.2s ease",
            },
            "nav-link-selected": {
                "background-color": "rgba(0,151,167,0.2)",
                "color": "white",
                "font-weight": "500",
            },
        }
    )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Settings Section (only show for relevant pages)
    if selected in ["Konsultasi", "Beranda"]:
        st.markdown("""
        <div style="padding: 0 0.5rem;">
            <p style="color: rgba(255,255,255,0.4); font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem;">Pengaturan</p>
        </div>
        """, unsafe_allow_html=True)

        use_context = st.checkbox("Gunakan Konteks Dokumen", value=True, help="Aktifkan untuk mencari referensi dari dokumen yang sudah diupload")
        max_agents = st.slider("Jumlah Agen Maksimal", 1, 3, 2, help="Jumlah agen expert yang akan menjawab pertanyaan")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Session Section
    st.markdown("""
    <div style="padding: 0 0.5rem;">
        <p style="color: rgba(255,255,255,0.4); font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.5rem;">Sesi Aktif</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 0.75rem; margin: 0 0.5rem;">
        <p style="color: rgba(255,255,255,0.5); font-size: 0.7rem; margin: 0;">Session ID</p>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin: 0.25rem 0 0 0; font-family: monospace;">{st.session_state.session_id[:12]}...</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    if st.button("Mulai Sesi Baru", use_container_width=True, type="secondary"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.conversation_history = []
        st.session_state.prefilled_query = ""
        st.rerun()

    # Footer
    st.markdown(f"""
    <div style="position: absolute; bottom: 1rem; left: 0; right: 0; text-align: center;">
        <p style="color: rgba(255,255,255,0.3); font-size: 0.65rem; margin: 0;">v{APP_VERSION} · MS Hadianto</p>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====

if selected == "Beranda":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Komite Audit Intelligence</div>
        <div class="hero-subtitle">Sistem AI Multi-Agent untuk Konsultasi Ahli Komite Audit Indonesia</div>
        <div class="hero-description">
            Dapatkan jawaban komprehensif dari 6 agen ahli yang terspesialisasi dalam berbagai aspek
            Komite Audit — mulai dari penyusunan charter, perencanaan audit, review keuangan,
            kepatuhan regulasi, hingga pelaporan.
        </div>
        <div class="hero-badge">✨ Powered by RAG + Multi-Agent AI</div>
    </div>
    """, unsafe_allow_html=True)

    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Mulai Konsultasi", type="primary", use_container_width=True):
            st.session_state.prefilled_query = ""
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats Section
    st.markdown('<div class="section-title">Statistik Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Real-time metrics dari sistem</div>', unsafe_allow_html=True)

    # Fetch stats
    doc_stats = call_api("statistics/documents")

    cols = st.columns(4)

    total_docs = 0
    total_chunks = 0
    if doc_stats and doc_stats.get("statistics"):
        import pandas as pd
        df = pd.DataFrame(doc_stats["statistics"])
        if not df.empty:
            total_docs = int(df['total_documents'].sum())
            total_chunks = int(df['total_chunks'].sum())

    stats_data = [
        ("📄", str(total_docs), "Total Dokumen"),
        ("🧩", str(total_chunks), "Total Chunks"),
        ("🤖", "6", "Expert Agents"),
        ("⚡", "RAG", "Teknologi"),
    ]

    for col, (icon, value, label) in zip(cols, stats_data):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Expert Agents Section
    st.markdown('<div class="section-title">6 Expert Agents</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tim AI ahli yang siap menjawab pertanyaan Anda</div>', unsafe_allow_html=True)

    # First row of agents
    cols = st.columns(3)
    agents_list = list(AGENT_INFO.values())

    for idx, col in enumerate(cols):
        agent = agents_list[idx]
        with col:
            expertise_html = "".join([f"<li>{exp}</li>" for exp in agent["expertise"]])
            st.markdown(f"""
            <div class="agent-card-landing">
                <div class="agent-icon">{agent['icon']}</div>
                <h4>{agent['title']}</h4>
                <p>{agent['desc']}</p>
                <ul>{expertise_html}</ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Second row of agents
    cols = st.columns(3)
    for idx, col in enumerate(cols):
        agent = agents_list[idx + 3]
        with col:
            expertise_html = "".join([f"<li>{exp}</li>" for exp in agent["expertise"]])
            st.markdown(f"""
            <div class="agent-card-landing">
                <div class="agent-icon">{agent['icon']}</div>
                <h4>{agent['title']}</h4>
                <p>{agent['desc']}</p>
                <ul>{expertise_html}</ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # How It Works Section
    st.markdown("""
    <div class="how-it-works">
        <div class="section-title" style="margin-bottom: 0.5rem;">Cara Kerja Sistem</div>
        <div class="section-subtitle" style="margin-bottom: 1.5rem;">4 langkah sederhana untuk mendapatkan jawaban ahli</div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    steps = [
        ("1", "Ajukan Pertanyaan", "Ketik pertanyaan Anda tentang Komite Audit"),
        ("2", "AI Routing", "Sistem memilih expert agent yang paling relevan"),
        ("3", "RAG Analysis", "Pencarian konteks dari dokumen & knowledge base"),
        ("4", "Jawaban Ahli", "Dapatkan respons komprehensif dari expert"),
    ]

    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-number">{num}</div>
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Example Queries Section
    st.markdown('<div class="section-title">Contoh Pertanyaan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Klik untuk langsung mencoba</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, example in enumerate(EXAMPLE_QUERIES):
        with cols[idx % 2]:
            if st.button(f"💬 {example['query']}", key=f"example_{idx}", use_container_width=True):
                st.session_state.prefilled_query = example['query']
                st.rerun()

    # Footer Section
    st.markdown(f"""
    <div class="app-footer">
        <div class="footer-disclaimer">
            <strong>⚠️ Disclaimer:</strong> Sistem ini merupakan alat bantu berbasis AI untuk memberikan informasi umum
            seputar Komite Audit. Hasil konsultasi bukan merupakan nasihat hukum atau profesional yang mengikat.
            Pengguna disarankan untuk tetap berkonsultasi dengan ahli profesional untuk keputusan bisnis yang penting.
        </div>
        <div class="footer-divider"></div>
        <div class="footer-developer">
            Developed by <strong>MS Hadianto</strong> · KIM Consulting · HADIANT Platform
        </div>
        <div class="footer-version">
            Komite Audit Intelligence System v{APP_VERSION} · © 2024
        </div>
    </div>
    """, unsafe_allow_html=True)

elif selected == "Konsultasi":
    st.markdown('<div class="main-header">Konsultasi Komite Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sistem multi-agen cerdas untuk menjawab pertanyaan seputar tata kelola dan praktik Komite Audit</div>', unsafe_allow_html=True)

    # Expert Agents Panel
    with st.expander("Lihat Expert Agents yang Tersedia", expanded=False):
        agents_data = call_api("agents")
        if agents_data:
            cols = st.columns(3)
            for idx, (key, agent) in enumerate(agents_data.get("agents", {}).items()):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>{agent['name']}</h4>
                        <p>{agent['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # Query Section
    st.markdown('<div class="section-header">Ajukan Pertanyaan</div>', unsafe_allow_html=True)

    # Use prefilled query if available
    default_query = st.session_state.prefilled_query if st.session_state.prefilled_query else ""

    user_query = st.text_area(
        "Pertanyaan Anda",
        value=default_query,
        placeholder="Contoh: Bagaimana peran Komite Audit dalam mengawasi efektivitas pengendalian internal perusahaan?",
        height=100,
        label_visibility="collapsed"
    )

    # Clear prefilled query after use
    if st.session_state.prefilled_query:
        st.session_state.prefilled_query = ""

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        submit_button = st.button("Kirim", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("Hapus Riwayat", use_container_width=True)

    if clear_button:
        st.session_state.conversation_history = []
        st.rerun()

    # Process query
    if submit_button and user_query:
        with st.spinner("Memproses pertanyaan Anda..."):
            result = call_api(
                "query",
                method="POST",
                json={
                    "query": user_query,
                    "session_id": st.session_state.session_id,
                    "use_context": use_context,
                    "max_agents": max_agents
                }
            )

            if result and result.get("success"):
                st.session_state.conversation_history.append({
                    "query": user_query,
                    "response": result.get("response"),
                    "agents_used": result.get("agents_used", []),
                    "processing_time": result.get("processing_time_ms"),
                    "context_count": result.get("context_count", 0),
                    "timestamp": datetime.now()
                })

    # Conversation History
    if st.session_state.conversation_history:
        st.markdown('<div class="section-header">Riwayat Konsultasi</div>', unsafe_allow_html=True)

        for idx, conv in enumerate(reversed(st.session_state.conversation_history)):
            st.markdown(f"""
            <div class="query-box">
                <strong>Pertanyaan:</strong> {conv['query']}
                <div class="query-meta">
                    {conv['timestamp'].strftime('%d %B %Y, %H:%M')} ·
                    Agen: {', '.join(conv['agents_used'])} ·
                    Waktu proses: {conv['processing_time']}ms ·
                    Konteks: {conv['context_count']} dokumen
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="response-box">
                <strong>Jawaban:</strong><br><br>
                {conv['response']}
            </div>
            """, unsafe_allow_html=True)

elif selected == "Dokumen":
    st.markdown('<div class="main-header">Manajemen Dokumen</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Unggah dan kelola dokumen referensi untuk basis pengetahuan sistem</div>', unsafe_allow_html=True)

    # Upload Section
    st.markdown('<div class="section-header">Unggah Dokumen</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Pilih file",
            type=['pdf', 'docx', 'txt', 'xlsx'],
            help="Format yang didukung: PDF, DOCX, TXT, XLSX",
            label_visibility="collapsed"
        )
    with col2:
        category = st.selectbox(
            "Kategori",
            ["Deteksi Otomatis", "Audit Committee Charter", "Audit Planning",
             "Financial Review", "Regulatory", "Banking", "Reporting"],
            label_visibility="collapsed"
        )

    if st.button("Unggah & Proses", type="primary") and uploaded_file:
        with st.spinner("Mengunggah dan memproses dokumen..."):
            files = {"file": uploaded_file}
            data = {"category": category if category != "Deteksi Otomatis" else None}

            result = call_api(
                "upload",
                method="POST",
                files=files,
                data=data
            )

            if result and result.get("success"):
                st.success(f"Dokumen berhasil diunggah. {result.get('message')}")
            else:
                st.error("Gagal mengunggah dokumen")

    st.markdown("---")

    # Document List
    st.markdown('<div class="section-header">Daftar Dokumen</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox(
            "Filter Kategori",
            ["Semua", "Audit Committee Charter", "Audit Planning",
             "Financial Review", "Regulatory", "Banking", "Reporting", "General"]
        )
    with col2:
        filter_status = st.selectbox(
            "Filter Status",
            ["Semua", "uploaded", "processing", "processed", "error"]
        )
    with col3:
        limit = st.number_input("Tampilkan", min_value=10, max_value=100, value=50)

    params = {
        "limit": limit,
        "category": filter_category if filter_category != "Semua" else None,
        "status": filter_status if filter_status != "Semua" else None
    }

    documents_data = call_api("documents", params=params)

    if documents_data and documents_data.get("documents"):
        documents = documents_data["documents"]

        for doc in documents:
            status_class = f"status-{doc['status']}" if doc['status'] in ['processed', 'processing', 'error'] else 'status-processing'

            with st.expander(f"{doc['filename']}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                    **Kategori:** {doc.get('category', 'Tidak ditentukan')}
                    **Tanggal Unggah:** {doc['upload_date']}
                    **Ukuran:** {format_bytes(doc['file_size'])}
                    **Jumlah Chunk:** {doc.get('total_chunks', 0)}
                    """)
                    if doc.get('tags'):
                        st.markdown(f"**Tags:** {', '.join(doc['tags'])}")

                with col2:
                    st.markdown(f'<span class="{status_class}">{doc["status"].upper()}</span>', unsafe_allow_html=True)
                    st.write("")
                    if st.button("Hapus", key=f"del_{doc['id']}"):
                        if call_api(f"documents/{doc['id']}", method="DELETE"):
                            st.success("Dokumen berhasil dihapus")
                            st.rerun()
    else:
        st.info("Belum ada dokumen. Unggah dokumen untuk memulai.")

elif selected == "Analitik":
    st.markdown('<div class="main-header">Dashboard Analitik</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Statistik dokumen dan performa sistem multi-agen</div>', unsafe_allow_html=True)

    doc_stats = call_api("statistics/documents")
    agent_stats = call_api("statistics/agents")

    # Document Statistics
    st.markdown('<div class="section-header">Statistik Dokumen</div>', unsafe_allow_html=True)

    if doc_stats and doc_stats.get("statistics"):
        stats = doc_stats["statistics"]
        import pandas as pd
        df = pd.DataFrame(stats)

        # Summary Metrics
        cols = st.columns(4)
        metrics = [
            ("Total Dokumen", df['total_documents'].sum() if not df.empty else 0),
            ("Total Chunk", df['total_chunks'].sum() if not df.empty else 0),
            ("Rata-rata Ukuran", format_bytes(df['avg_file_size'].mean()) if not df.empty else "0 B"),
            ("Kategori", len(df) if not df.empty else 0)
        ]

        for col, (label, value) in zip(cols, metrics):
            with col:
                st.metric(label, value)

        st.write("")

        if not df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    df,
                    x='category',
                    y='total_documents',
                    title='Dokumen per Kategori',
                    color_discrete_sequence=['#003366']
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Inter, sans-serif"),
                    title_font=dict(size=14, color='#003366'),
                    showlegend=False,
                    xaxis_title="",
                    yaxis_title="Jumlah Dokumen"
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.pie(
                    df,
                    values='total_chunks',
                    names='category',
                    title='Distribusi Chunk',
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Inter, sans-serif"),
                    title_font=dict(size=14, color='#003366'),
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data statistik dokumen.")

    st.markdown("---")

    # Agent Performance
    st.markdown('<div class="section-header">Performa Agen</div>', unsafe_allow_html=True)

    if agent_stats and agent_stats.get("statistics"):
        stats = agent_stats["statistics"]
        import pandas as pd
        df = pd.DataFrame(stats)

        if not df.empty:
            fig = go.Figure(data=[
                go.Bar(
                    name='Total Eksekusi',
                    x=df['agent_name'],
                    y=df['total_executions'],
                    marker_color='#003366'
                ),
                go.Bar(
                    name='Rata-rata Waktu (ms)',
                    x=df['agent_name'],
                    y=df['avg_execution_time'],
                    marker_color='#0097a7'
                )
            ])
            fig.update_layout(
                title='Metrik Performa Agen',
                barmode='group',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif"),
                title_font=dict(size=14, color='#003366'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Success Rate
            fig = px.bar(
                df,
                x='agent_name',
                y='success_rate',
                title='Tingkat Keberhasilan Agen',
                color='success_rate',
                color_continuous_scale=['#fce8e6', '#e6f4ea'],
                range_color=[0, 1]
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif"),
                title_font=dict(size=14, color='#003366'),
                showlegend=False,
                xaxis_title="",
                yaxis_title="Success Rate",
                yaxis=dict(tickformat='.0%')
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data performa agen.")

elif selected == "Tentang":
    st.markdown('<div class="main-header">Tentang Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Informasi mengenai Komite Audit Intelligence System</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h3>Komite Audit Intelligence</h3>
        <p>Sistem kecerdasan buatan berbasis multi-agen untuk memberikan konsultasi ahli seputar tata kelola dan praktik Komite Audit di Indonesia.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Kapabilitas Sistem</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Arsitektur Multi-Agen**

        Sistem menggunakan 6 agen ahli yang terspesialisasi dalam berbagai aspek Komite Audit:

        1. **Charter Expert** — Penyusunan Audit Committee Charter
        2. **Planning Expert** — Perencanaan dan pelaksanaan audit
        3. **Financial Review Expert** — Review laporan keuangan
        4. **Regulatory Expert** — Kepatuhan regulasi (OJK, PSAK, SPAP)
        5. **Banking Expert** — Spesifik sektor perbankan
        6. **Reporting Expert** — Pelaporan dan pengungkapan
        """)

    with col2:
        st.markdown("""
        **Teknologi**

        - **Backend:** FastAPI + Python
        - **Frontend:** Streamlit
        - **LLM:** Groq API (Llama 3.3 70B) + GLM (Zhipu AI)
        - **Vector Store:** Supabase + pgvector
        - **Embeddings:** Sentence Transformers

        **Fitur Utama**

        - Retrieval Augmented Generation (RAG)
        - Pencarian semantik berbasis vektor
        - Routing cerdas ke agen yang relevan
        - Sintesis jawaban dari multi-agen
        """)

    st.markdown("---")

    st.markdown('<div class="section-header">Status Sistem</div>', unsafe_allow_html=True)

    health = call_api("health")
    if health:
        col1, col2, col3 = st.columns(3)
        with col1:
            status = health.get('status', 'Unknown')
            st.metric("Status", status.upper())
        with col2:
            st.metric("Database", health.get('database', 'Unknown').upper())
        with col3:
            st.metric("Model LLM", health.get('llm_model', 'Unknown'))

    st.markdown("---")

    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0; color: #5f6368;">
        <p style="margin: 0; font-size: 0.85rem;">Komite Audit Intelligence System v{APP_VERSION}</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Developed by MS Hadianto · KIM Consulting · HADIANT Platform</p>
    </div>
    """, unsafe_allow_html=True)
