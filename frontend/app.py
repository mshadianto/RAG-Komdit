"""
Streamlit Frontend for RAG Komite Audit System
User-friendly interface for the multi-agent RAG system
"""
import streamlit as st
import requests
import uuid
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="RAG Komite Audit System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }
    .query-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .response-box {
        background-color: #f9f9f9;
        border-left: 4px solid #2ca02c;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def call_api(endpoint: str, method: str = "GET", **kwargs):
    """Call API endpoint"""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        elif method == "DELETE":
            response = requests.delete(url, **kwargs)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    selected = option_menu(
        menu_title=None,
        options=["Chat", "Documents", "Analytics", "About"],
        icons=["chat-dots", "folder", "graph-up", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    use_context = st.checkbox("Use Document Context", value=True)
    max_agents = st.slider("Max Agents", 1, 3, 2)
    
    st.markdown("---")
    st.markdown("### 📝 Session Info")
    st.caption(f"Session ID: {st.session_state.session_id[:8]}...")
    
    if st.button("🔄 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.conversation_history = []
        st.rerun()

# Main content based on selection
if selected == "Chat":
    st.markdown('<div class="main-header">💬 Chat dengan Expert Komite Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-Agent RAG System untuk Pertanyaan seputar Komite Audit</div>', unsafe_allow_html=True)
    
    # Display available agents
    with st.expander("🤖 Available Expert Agents"):
        agents_data = call_api("agents")
        if agents_data:
            cols = st.columns(3)
            for idx, (key, agent) in enumerate(agents_data.get("agents", {}).items()):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>{agent['name']}</h4>
                        <p style="font-size: 0.9rem;">{agent['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Chat interface
    st.markdown("### 💭 Ask Your Question")
    
    # Query input
    user_query = st.text_area(
        "Your Question:",
        placeholder="Contoh: Jelaskan peran Komite Audit dalam proses audit planning...",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        submit_button = st.button("🚀 Submit", type="primary")
    with col2:
        clear_button = st.button("🗑️ Clear History")
    
    if clear_button:
        st.session_state.conversation_history = []
        st.rerun()
    
    # Process query
    if submit_button and user_query:
        with st.spinner("🤔 Processing your query..."):
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
                    "timestamp": datetime.now()
                })
    
    # Display conversation history
    if st.session_state.conversation_history:
        st.markdown("---")
        st.markdown("### 📜 Conversation History")
        
        for idx, conv in enumerate(reversed(st.session_state.conversation_history)):
            with st.container():
                st.markdown(f"""
                <div class="query-box">
                    <strong>Q: </strong>{conv['query']}<br>
                    <small style="color: #666;">
                        {conv['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} | 
                        Agents: {', '.join(conv['agents_used'])} | 
                        {conv['processing_time']}ms
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="response-box">
                    <strong>A: </strong>{conv['response']}
                </div>
                """, unsafe_allow_html=True)
                
                # Feedback
                col1, col2 = st.columns([1, 5])
                with col1:
                    rating = st.selectbox(
                        "Rate this response:",
                        [1, 2, 3, 4, 5],
                        key=f"rating_{idx}",
                        label_visibility="collapsed"
                    )
                with col2:
                    if st.button("Submit Feedback", key=f"feedback_{idx}"):
                        st.success("Thank you for your feedback!")
                
                st.markdown("---")

elif selected == "Documents":
    st.markdown('<div class="main-header">📁 Document Management</div>', unsafe_allow_html=True)
    
    # Upload section
    st.markdown("### 📤 Upload Documents")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'txt', 'xlsx'],
        help="Supported formats: PDF, DOCX, TXT, XLSX"
    )
    
    category = st.selectbox(
        "Category (Optional)",
        ["Auto-detect", "Audit Committee Charter", "Audit Planning", 
         "Financial Review", "Regulatory", "Banking", "Reporting"]
    )
    
    if st.button("Upload & Process") and uploaded_file:
        with st.spinner("Uploading and processing..."):
            files = {"file": uploaded_file}
            data = {"category": category if category != "Auto-detect" else None}
            
            result = call_api(
                "upload",
                method="POST",
                files=files,
                data=data
            )
            
            if result and result.get("success"):
                st.success(f"✅ {result.get('message')}")
            else:
                st.error("Failed to upload document")
    
    st.markdown("---")
    
    # List documents
    st.markdown("### 📚 Uploaded Documents")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All", "Audit Committee Charter", "Audit Planning", 
             "Financial Review", "Regulatory", "Banking", "Reporting", "General"]
        )
    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "uploaded", "processing", "processed", "error"]
        )
    with col3:
        limit = st.number_input("Limit", min_value=10, max_value=100, value=50)
    
    # Fetch documents
    params = {
        "limit": limit,
        "category": filter_category if filter_category != "All" else None,
        "status": filter_status if filter_status != "All" else None
    }
    
    documents_data = call_api("documents", params=params)
    
    if documents_data and documents_data.get("documents"):
        documents = documents_data["documents"]
        
        for doc in documents:
            with st.expander(f"📄 {doc['filename']} - {doc['status'].upper()}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Category:** {doc.get('category', 'N/A')}")
                    st.write(f"**Uploaded:** {doc['upload_date']}")
                    st.write(f"**Size:** {doc['file_size']} bytes")
                    st.write(f"**Chunks:** {doc.get('total_chunks', 0)}")
                    if doc.get('tags'):
                        st.write(f"**Tags:** {', '.join(doc['tags'])}")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{doc['id']}"):
                        if call_api(f"documents/{doc['id']}", method="DELETE"):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("No documents found. Upload some documents to get started!")

elif selected == "Analytics":
    st.markdown('<div class="main-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Get statistics
    doc_stats = call_api("statistics/documents")
    agent_stats = call_api("statistics/agents")
    
    # Document statistics
    st.markdown("### 📈 Document Statistics")
    if doc_stats and doc_stats.get("statistics"):
        stats = doc_stats["statistics"]
        
        # Create DataFrame for plotting
        import pandas as pd
        df = pd.DataFrame(stats)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Documents by category
            if not df.empty:
                fig = px.bar(
                    df,
                    x='category',
                    y='total_documents',
                    title='Documents by Category',
                    color='total_documents',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Chunks distribution
            if not df.empty:
                fig = px.pie(
                    df,
                    values='total_chunks',
                    names='category',
                    title='Chunks Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Summary cards
        st.markdown("### 📋 Summary")
        cols = st.columns(4)
        with cols[0]:
            total_docs = df['total_documents'].sum() if not df.empty else 0
            st.metric("Total Documents", total_docs)
        with cols[1]:
            total_chunks = df['total_chunks'].sum() if not df.empty else 0
            st.metric("Total Chunks", total_chunks)
        with cols[2]:
            avg_size = df['avg_file_size'].mean() if not df.empty else 0
            st.metric("Avg File Size", f"{avg_size:.0f} bytes")
        with cols[3]:
            categories = len(df) if not df.empty else 0
            st.metric("Categories", categories)
    
    st.markdown("---")
    
    # Agent performance
    st.markdown("### 🤖 Agent Performance")
    if agent_stats and agent_stats.get("statistics"):
        stats = agent_stats["statistics"]
        
        import pandas as pd
        df = pd.DataFrame(stats)
        
        if not df.empty:
            # Agent executions
            fig = go.Figure(data=[
                go.Bar(
                    name='Total Executions',
                    x=df['agent_name'],
                    y=df['total_executions'],
                    marker_color='lightblue'
                ),
                go.Bar(
                    name='Avg Execution Time (ms)',
                    x=df['agent_name'],
                    y=df['avg_execution_time'],
                    marker_color='lightgreen'
                )
            ])
            fig.update_layout(
                title='Agent Performance Metrics',
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Success rate
            fig = px.bar(
                df,
                x='agent_name',
                y='success_rate',
                title='Agent Success Rate',
                color='success_rate',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)

elif selected == "About":
    st.markdown('<div class="main-header">ℹ️ About RAG Komite Audit System</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎯 Sistem RAG Multi-Agent untuk Expertise Komite Audit
    
    ### Fitur Utama:
    - **Multi-Agent Architecture**: 6 expert agents yang specialized dalam berbagai aspek Komite Audit
    - **RAG (Retrieval Augmented Generation)**: Menggunakan dokumen Anda sendiri sebagai knowledge base
    - **Vector Search**: Pencarian semantik menggunakan pgvector di Supabase
    - **Free Tier**: Menggunakan Groq API (free), Supabase (free tier), dan model embedding open-source
    
    ### Expert Agents:
    1. **Audit Committee Charter Expert** - Penyusunan charter dan governance
    2. **Audit Planning & Execution Expert** - Perencanaan dan pelaksanaan audit
    3. **Financial Reporting Review Expert** - Review laporan keuangan
    4. **Regulatory Compliance Expert** - Regulasi dan compliance (UU Pasar Modal, PSAK, SPAP)
    5. **Banking Audit Committee Expert** - Khusus untuk sektor perbankan
    6. **Reporting & Disclosure Expert** - Pelaporan dan pengungkapan
    
    ### Teknologi:
    - **Backend**: FastAPI + Python 3.10+
    - **Frontend**: Streamlit
    - **LLM**: Groq API (Llama 3.1 70B)
    - **Vector Store**: Supabase + pgvector
    - **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
    
    ### Developer:
    Sopian - Senior Audit Committee Member at BPKH  
    KIM Consulting | HADIANT Platform
    
    ### Version:
    v1.0.0 - January 2026
    """)
    
    st.markdown("---")
    
    # System health check
    st.markdown("### 🏥 System Health")
    health = call_api("health")
    if health:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"✅ Status: {health.get('status', 'Unknown')}")
        with col2:
            st.info(f"🗄️ Database: {health.get('database', 'Unknown')}")
        with col3:
            st.info(f"🤖 LLM Model: {health.get('llm_model', 'Unknown')}")
