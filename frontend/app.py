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
    page_title="KAMI - Komite Audit Multi-Intelligence",
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

# Midnight Vault Dark Theme CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Styles - Midnight Vault Theme */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0E1117 !important;
        color: #E0E0E0 !important;
    }

    /* Main content text colors */
    .stApp p, .stApp li, .stApp span, .stApp div {
        color: #E0E0E0;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #FFFFFF !important;
    }

    .stApp strong, .stApp b {
        color: #00C6FF !important;
    }

    .stMarkdown p, .stMarkdown li {
        color: #B0B0B0 !important;
    }

    .stMarkdown strong, .stMarkdown b {
        color: #00C6FF !important;
    }

    /* Ensure all text is readable */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        color: #B0B0B0 !important;
    }

    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] b {
        color: #00C6FF !important;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #FFFFFF !important;
    }

    /* Color Variables - Midnight Vault Theme */
    :root {
        --bg-primary: #0E1117;
        --bg-secondary: #141A23;
        --bg-card: rgba(30, 39, 50, 0.5);
        --bg-card-hover: rgba(30, 39, 50, 0.8);
        --accent-cyan: #00C6FF;
        --accent-blue: #0072FF;
        --accent-green: #00FF41;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
        --text-muted: #6B7280;
        --border-color: rgba(0, 198, 255, 0.2);
        --border-hover: rgba(0, 198, 255, 0.4);
        --glow-cyan: rgba(0, 198, 255, 0.6);
    }

    /* Sidebar Styling - Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: #0a0e14 !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 198, 255, 0.2) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #0a0e14 !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: #B0B0B0 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(0, 198, 255, 0.2) !important;
    }

    [data-testid="stSidebar"] label {
        color: #B0B0B0 !important;
    }

    [data-testid="stSidebar"] .stCheckbox label span {
        color: #B0B0B0 !important;
    }

    [data-testid="stSidebar"] .stSlider label {
        color: #B0B0B0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #B0B0B0 !important;
    }

    /* Sidebar widget text */
    section[data-testid="stSidebar"] * {
        color: #E0E0E0;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #00C6FF !important;
    }

    /* Option Menu in Sidebar - Force Dark Theme */
    [data-testid="stSidebar"] .nav-link,
    .nav-link {
        color: #B0B0B0 !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] .nav-link:hover,
    .nav-link:hover {
        color: #00C6FF !important;
        background-color: rgba(0, 198, 255, 0.1) !important;
    }

    [data-testid="stSidebar"] .nav-link-selected,
    .nav-link-selected {
        color: #00C6FF !important;
        background-color: rgba(0, 198, 255, 0.15) !important;
    }

    /* Force dark background on option menu container */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stSidebar"] .css-1cypcdb,
    [data-testid="stSidebar"] .css-1v0mbdj,
    [data-testid="stSidebar"] .st-emotion-cache-1cypcdb,
    [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj,
    [data-testid="stSidebar"] [data-baseweb="tab-list"],
    [data-testid="stSidebar"] .css-pkbazv,
    [data-testid="stSidebar"] .st-emotion-cache-pkbazv {
        background-color: #0a0e14 !important;
    }

    /* Option menu specific overrides */
    .css-1adrfps, .st-emotion-cache-1adrfps,
    .css-z5fcl4, .st-emotion-cache-z5fcl4 {
        background-color: #0a0e14 !important;
    }

    div[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNav"] > ul {
        background-color: #0a0e14 !important;
    }

    /* Force ALL sidebar elements to dark background */
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] nav,
    [data-testid="stSidebar"] ul,
    [data-testid="stSidebar"] li {
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] > div > div {
        background-color: #0a0e14 !important;
    }

    /* streamlit-option-menu specific fix */
    [data-testid="stSidebar"] iframe + div,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .element-container {
        background-color: transparent !important;
    }

    /* Checkbox in sidebar */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        color: #B0B0B0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        color: #B0B0B0 !important;
    }

    /* Slider in sidebar */
    [data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
    [data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
        color: #6B7280 !important;
    }

    [data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
        color: #00C6FF !important;
    }

    /* Chat Message Styling */
    .stChatMessage {
        background-color: rgba(30, 39, 50, 0.5) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 150, 255, 0.2) !important;
    }

    /* Button Styling - Gradient */
    .stButton > button {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        box-shadow: 0px 0px 20px rgba(0, 198, 255, 0.6) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Secondary Button */
    .stButton > button[kind="secondary"],
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(0, 198, 255, 0.1) !important;
        border: 1px solid rgba(0, 198, 255, 0.4) !important;
        color: #00C6FF !important;
    }

    .stButton > button[kind="secondary"]:hover,
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 198, 255, 0.2) !important;
        border-color: #00C6FF !important;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.3) !important;
    }

    /* Pulse Animation */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 65, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 65, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 65, 0); }
    }

    .pulse-dot {
        height: 10px;
        width: 10px;
        background-color: #00FF41;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }

    /* ===== LANDING PAGE STYLES ===== */

    /* Hero Section - Vault Style */
    .hero-section {
        background: linear-gradient(135deg, rgba(30, 39, 50, 0.9) 0%, rgba(10, 15, 25, 0.95) 100%);
        border: 1px solid rgba(0, 198, 255, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.1);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 50%, #00C6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    .hero-tagline {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #00FF41;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }

    .hero-description {
        font-size: 1rem;
        color: #E0E0E0;
        max-width: 700px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.7;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(0, 198, 255, 0.15);
        border: 1px solid rgba(0, 198, 255, 0.3);
        padding: 0.5rem 1.25rem;
        border-radius: 25px;
        font-size: 0.85rem;
        color: #00C6FF;
        margin-top: 0.5rem;
    }

    .hero-engine {
        background: rgba(0, 198, 255, 0.05);
        padding: 12px 20px;
        border-left: 4px solid #0072FF;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #B0B0B0;
        margin-top: 1.5rem;
        display: inline-block;
    }

    /* Agent Cards for Landing - Dark Theme */
    .agent-card-landing {
        background: rgba(30, 39, 50, 0.6);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        cursor: default;
    }

    .agent-card-landing:hover {
        background: rgba(30, 39, 50, 0.9);
        box-shadow: 0 8px 30px rgba(0, 198, 255, 0.15);
        transform: translateY(-3px);
        border-color: rgba(0, 198, 255, 0.4);
    }

    .agent-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .agent-card-landing h4 {
        color: #00C6FF;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .agent-card-landing p {
        color: #B0B0B0;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 0.75rem;
    }

    .agent-card-landing ul {
        margin: 0;
        padding-left: 1.2rem;
        color: #6B7280;
        font-size: 0.8rem;
    }

    .agent-card-landing li {
        margin-bottom: 0.25rem;
    }

    /* How It Works Section - Dark Theme */
    .how-it-works {
        background: rgba(20, 26, 35, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }

    .step-card {
        text-align: center;
        padding: 1.5rem 1rem;
    }

    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 1rem auto;
        box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);
    }

    .step-title {
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .step-desc {
        color: #6B7280;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* Stats Cards - Dark Theme */
    .stat-card {
        background: rgba(30, 39, 50, 0.6);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        box-shadow: 0 4px 20px rgba(0, 198, 255, 0.2);
        border-color: rgba(0, 198, 255, 0.3);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }

    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Section Headers - Dark Theme */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* ===== MAIN CONTENT STYLES ===== */

    /* Main Header */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #00C6FF;
        text-align: left;
        padding: 0.5rem 0;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
    }

    .sub-header {
        font-size: 1rem;
        color: #6B7280;
        text-align: left;
        padding-bottom: 1.5rem;
        font-weight: 400;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00C6FF;
        display: inline-block;
    }

    /* Agent Cards */
    .agent-card {
        background-color: rgba(30, 39, 50, 0.6);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 10px;
        padding: 1.25rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .agent-card:hover {
        box-shadow: 0 4px 15px rgba(0, 198, 255, 0.2);
        border-color: rgba(0, 198, 255, 0.3);
    }

    .agent-card h4 {
        color: #00C6FF;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .agent-card p {
        color: #B0B0B0;
        font-size: 0.85rem;
        line-height: 1.5;
        margin: 0;
    }

    /* Query Box */
    .query-box {
        background-color: rgba(30, 39, 50, 0.6);
        border-left: 3px solid #00C6FF;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }

    .query-box strong {
        color: #00C6FF;
        font-weight: 600;
    }

    .query-meta {
        color: #6B7280;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }

    /* Response Box */
    .response-box {
        background-color: rgba(20, 26, 35, 0.8);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-left: 3px solid #00FF41;
        padding: 1.25rem;
        margin: 0.75rem 0 1.5rem 0;
        border-radius: 0 10px 10px 0;
        line-height: 1.7;
        color: #E0E0E0;
    }

    .response-box strong {
        color: #00FF41;
        font-weight: 600;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 39, 50, 0.6);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #00C6FF;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }

    /* Document Card */
    .doc-card {
        background: rgba(30, 39, 50, 0.6);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .doc-title {
        font-weight: 600;
        color: #00C6FF;
    }

    .doc-meta {
        font-size: 0.85rem;
        color: #6B7280;
    }

    /* Status Badges */
    .status-processed {
        background-color: rgba(0, 255, 65, 0.15);
        color: #00FF41;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid rgba(0, 255, 65, 0.3);
    }

    .status-processing {
        background-color: rgba(255, 170, 0, 0.15);
        color: #FFAA00;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid rgba(255, 170, 0, 0.3);
    }

    .status-error {
        background-color: rgba(255, 65, 65, 0.15);
        color: #FF4141;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid rgba(255, 65, 65, 0.3);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 114, 255, 0.2) 0%, rgba(0, 198, 255, 0.1) 100%);
        border: 1px solid rgba(0, 198, 255, 0.3);
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .info-box h3 {
        margin: 0 0 0.5rem 0;
        font-weight: 600;
        color: #00C6FF;
    }

    .info-box p {
        margin: 0;
        color: #B0B0B0;
        font-size: 0.9rem;
    }

    /* Table Styling */
    .dataframe {
        border: none !important;
        background: transparent !important;
    }

    .dataframe th {
        background-color: rgba(0, 114, 255, 0.3) !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    .dataframe td {
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: #E0E0E0 !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: #00C6FF !important;
        background: rgba(30, 39, 50, 0.6) !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] {
        background-color: rgba(30, 39, 50, 0.4) !important;
        border: 1px solid rgba(0, 198, 255, 0.15) !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary {
        color: #00C6FF !important;
    }

    [data-testid="stExpander"] summary span {
        color: #00C6FF !important;
    }

    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        color: #B0B0B0 !important;
    }

    /* Text Input Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(30, 39, 50, 0.8) !important;
        border: 1px solid rgba(0, 198, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00C6FF !important;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.3) !important;
    }

    /* Select Box Styling */
    .stSelectbox > div > div {
        background-color: rgba(30, 39, 50, 0.8) !important;
        border: 1px solid rgba(0, 198, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    /* Checkbox Styling */
    .stCheckbox > label {
        color: #B0B0B0 !important;
    }

    /* Slider Styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%) !important;
    }

    /* File Uploader */
    .stFileUploader > div {
        background-color: rgba(30, 39, 50, 0.6) !important;
        border: 2px dashed rgba(0, 198, 255, 0.3) !important;
        border-radius: 12px !important;
    }

    .stFileUploader > div:hover {
        border-color: #00C6FF !important;
    }

    /* Footer Styling */
    .app-footer {
        background: linear-gradient(135deg, rgba(30, 39, 50, 0.9) 0%, rgba(10, 15, 25, 0.95) 100%);
        border: 1px solid rgba(0, 198, 255, 0.2);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
    }

    .footer-disclaimer {
        font-size: 0.8rem;
        color: #B0B0B0;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto 1.5rem auto;
        padding: 1rem;
        background: rgba(0, 198, 255, 0.05);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 8px;
    }

    .footer-developer {
        font-size: 0.9rem;
        color: #E0E0E0;
        margin-bottom: 0.5rem;
    }

    .footer-version {
        font-size: 0.75rem;
        color: #6B7280;
    }

    .footer-divider {
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        margin: 1rem auto;
    }

    /* Plotly Chart Background Fix */
    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }

    /* Number Input */
    .stNumberInput > div > div > input {
        background-color: rgba(30, 39, 50, 0.8) !important;
        border: 1px solid rgba(0, 198, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    /* Metric Widget Override */
    [data-testid="stMetricValue"] {
        color: #00C6FF !important;
    }

    [data-testid="stMetricLabel"] {
        color: #6B7280 !important;
    }

    /* Labels and Help Text */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stSlider label, .stCheckbox label, .stNumberInput label,
    .stFileUploader label {
        color: #B0B0B0 !important;
    }

    /* Widget help text */
    .stTooltipIcon {
        color: #6B7280 !important;
    }

    /* Spinner text */
    .stSpinner > div {
        color: #00C6FF !important;
    }

    /* Divider / horizontal rule */
    hr {
        border-color: rgba(0, 198, 255, 0.2) !important;
    }

    /* Links */
    a {
        color: #00C6FF !important;
    }

    a:hover {
        color: #00FF41 !important;
    }

    /* Success/Error/Info Messages */
    .stSuccess {
        background-color: rgba(0, 255, 65, 0.1) !important;
        border: 1px solid rgba(0, 255, 65, 0.3) !important;
        color: #00FF41 !important;
    }

    .stError {
        background-color: rgba(255, 65, 65, 0.1) !important;
        border: 1px solid rgba(255, 65, 65, 0.3) !important;
        color: #FF4141 !important;
    }

    .stInfo {
        background-color: rgba(0, 198, 255, 0.1) !important;
        border: 1px solid rgba(0, 198, 255, 0.3) !important;
        color: #00C6FF !important;
    }

    /* Welcome Vault Box */
    .welcome-vault {
        background: linear-gradient(135deg, rgba(30, 39, 50, 0.8) 0%, rgba(10, 15, 25, 0.9) 100%);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(0, 198, 255, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }

    .welcome-vault h1 {
        color: #00C6FF;
        font-size: 2.2rem;
        margin-bottom: 0;
    }

    .welcome-vault .status {
        color: #00FF41;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        margin-top: 5px;
    }

    .welcome-vault hr {
        border: 0;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 20px 0;
    }

    .welcome-vault p {
        color: #E0E0E0;
        font-size: 1.1rem;
    }

    .welcome-vault .engine-info {
        background: rgba(0, 198, 255, 0.05);
        padding: 12px;
        border-left: 4px solid #0072FF;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #B0B0B0;
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
    # Logo and Title - Midnight Vault Style
    st.markdown("""
    <div style="padding: 1.5rem 1rem; text-align: center; border-bottom: 1px solid rgba(0, 198, 255, 0.15);">
        <div style="width: 55px; height: 55px; background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); border-radius: 14px; margin: 0 auto 0.75rem auto; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);">
            <span style="color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: -1px;">KAMI</span>
        </div>
        <h3 style="color: #00C6FF; font-weight: 600; margin: 0; font-size: 0.95rem;">Intelligence Hub</h3>
        <p style="color: #00FF41; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; margin-top: 0.5rem; letter-spacing: 0.3px;">[ Multi-Agent Expertise for Strategic Oversight ]</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Navigation Menu - Dark Theme
    selected = option_menu(
        menu_title=None,
        options=["Beranda", "Konsultasi", "Dokumen", "Analitik", "Tentang"],
        icons=["house-door", "chat-left-text", "folder2-open", "graph-up-arrow", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "#0a0e14"},
            "menu-title": {"color": "#00C6FF"},
            "icon": {"color": "#00C6FF", "font-size": "1rem"},
            "nav-link": {
                "font-size": "0.85rem",
                "text-align": "left",
                "margin": "0.15rem 0.5rem",
                "padding": "0.7rem 1rem",
                "color": "#B0B0B0",
                "background-color": "transparent",
                "border-radius": "8px",
                "transition": "all 0.3s ease",
                "border": "1px solid transparent",
            },
            "nav-link-selected": {
                "background-color": "rgba(0, 198, 255, 0.15)",
                "color": "#00C6FF",
                "font-weight": "600",
                "border": "1px solid rgba(0, 198, 255, 0.3)",
            },
        }
    )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Settings Section (only show for relevant pages)
    if selected in ["Konsultasi", "Beranda"]:
        st.markdown("""
        <div style="padding: 0 0.5rem;">
            <p style="color: #00C6FF; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem;">Pengaturan</p>
        </div>
        """, unsafe_allow_html=True)

        use_context = st.checkbox("Gunakan Konteks Dokumen", value=True, help="Aktifkan untuk mencari referensi dari dokumen yang sudah diupload")
        max_agents = st.slider("Jumlah Agen Maksimal", 1, 3, 2, help="Jumlah agen expert yang akan menjawab pertanyaan")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Session Section
    st.markdown("""
    <div style="padding: 0 0.5rem;">
        <p style="color: #00C6FF; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.5rem;">Sesi Aktif</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: rgba(0, 198, 255, 0.05); border: 1px solid rgba(0, 198, 255, 0.15); border-radius: 10px; padding: 0.75rem; margin: 0 0.5rem;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span class="pulse-dot" style="margin-right: 8px;"></span>
            <span style="color: #00FF41; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace;">ACTIVE</span>
        </div>
        <p style="color: #6B7280; font-size: 0.65rem; margin: 0;">Session ID</p>
        <p style="color: #00C6FF; font-size: 0.75rem; margin: 0.25rem 0 0 0; font-family: 'JetBrains Mono', monospace;">{st.session_state.session_id[:12]}...</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    if st.button("Terminate Session", use_container_width=True, type="secondary"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.conversation_history = []
        st.session_state.prefilled_query = ""
        st.rerun()

    # Footer
    st.markdown(f"""
    <div style="position: absolute; bottom: 1rem; left: 0; right: 0; text-align: center;">
        <p style="color: #6B7280; font-size: 0.6rem; margin: 0;">v{APP_VERSION} · <span style="color: #00C6FF;">Labbaik AI</span></p>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====

if selected == "Beranda":
    # Hero Section - Midnight Vault Style
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">KAMI</div>
        <div class="hero-subtitle">Komite Audit Multi-Intelligence</div>
        <div class="hero-tagline">[ Multi-Agent Expertise for Strategic Oversight ]</div>
        <div class="hero-description">
            Dapatkan jawaban komprehensif dari 6 agen ahli yang terspesialisasi dalam berbagai aspek
            Komite Audit — mulai dari penyusunan charter, perencanaan audit, review keuangan,
            kepatuhan regulasi, hingga pelaporan.
        </div>
        <div class="hero-badge">⚡ Powered by RAG + Multi-Agent AI</div>
        <div class="hero-engine"><b>Core Engine:</b> Multi-Agent RAG Orchestrator (Groq + Supabase)</div>
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
            Developed by <strong>MS Hadianto</strong> · Founder Labbaik AI
        </div>
        <div class="footer-version">
            KAMI v{APP_VERSION} · © 2026
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
                    color_discrete_sequence=['#00C6FF']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", color='#B0B0B0'),
                    title_font=dict(size=14, color='#00C6FF'),
                    showlegend=False,
                    xaxis_title="",
                    yaxis_title="Jumlah Dokumen",
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#B0B0B0'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#B0B0B0')
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.pie(
                    df,
                    values='total_chunks',
                    names='category',
                    title='Distribusi Chunk',
                    color_discrete_sequence=['#00C6FF', '#0072FF', '#00FF41', '#FFAA00', '#FF4141', '#B0B0B0']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", color='#B0B0B0'),
                    title_font=dict(size=14, color='#00C6FF'),
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
                    marker_color='#00C6FF'
                ),
                go.Bar(
                    name='Rata-rata Waktu (ms)',
                    x=df['agent_name'],
                    y=df['avg_execution_time'],
                    marker_color='#0072FF'
                )
            ])
            fig.update_layout(
                title='Metrik Performa Agen',
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color='#B0B0B0'),
                title_font=dict(size=14, color='#00C6FF'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#B0B0B0')),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#B0B0B0'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#B0B0B0')
            )
            st.plotly_chart(fig, use_container_width=True)

            # Success Rate
            fig = px.bar(
                df,
                x='agent_name',
                y='success_rate',
                title='Tingkat Keberhasilan Agen',
                color='success_rate',
                color_continuous_scale=['#FF4141', '#00FF41'],
                range_color=[0, 1]
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color='#B0B0B0'),
                title_font=dict(size=14, color='#00C6FF'),
                showlegend=False,
                xaxis_title="",
                yaxis_title="Success Rate",
                yaxis=dict(tickformat='.0%', gridcolor='rgba(255,255,255,0.1)', color='#B0B0B0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#B0B0B0')
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
    <div style="text-align: center; padding: 2rem 0;">
        <p style="margin: 0; font-size: 0.85rem; color: #00C6FF;">KAMI - Komite Audit Multi-Intelligence v{APP_VERSION}</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #6B7280;">Developed by <span style="color: #00FF41;">MS Hadianto</span> · Founder Labbaik AI · © 2026</p>
    </div>
    """, unsafe_allow_html=True)
