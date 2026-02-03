-- RAG Komite Audit System Database Schema
-- Run this in Supabase SQL Editor

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table - menyimpan metadata dokumen
CREATE TABLE IF NOT EXISTS komite_audit_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_date TIMESTAMP WITH TIME ZONE,
    total_chunks INTEGER DEFAULT 0,
    category VARCHAR(100),
    tags TEXT[],
    metadata JSONB,
    status VARCHAR(50) DEFAULT 'uploaded',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Embeddings table - menyimpan chunks dan vectors
CREATE TABLE IF NOT EXISTS komite_audit_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES komite_audit_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384), -- dimension untuk all-MiniLM-L6-v2
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversations table - menyimpan history conversations
CREATE TABLE IF NOT EXISTS komite_audit_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    user_query TEXT NOT NULL,
    agent_response TEXT,
    agents_used TEXT[],
    context_documents UUID[],
    similarity_scores FLOAT[],
    processing_time_ms INTEGER,
    feedback_rating INTEGER,
    feedback_comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent logs table - untuk monitoring agent performance
CREATE TABLE IF NOT EXISTS agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES komite_audit_conversations(id),
    agent_name VARCHAR(100),
    agent_role VARCHAR(100),
    input_text TEXT,
    output_text TEXT,
    execution_time_ms INTEGER,
    tokens_used INTEGER,
    status VARCHAR(50),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_documents_category ON komite_audit_documents(category);
CREATE INDEX IF NOT EXISTS idx_documents_status ON komite_audit_documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_upload_date ON komite_audit_documents(upload_date);

CREATE INDEX IF NOT EXISTS idx_embeddings_document_id ON komite_audit_embeddings(document_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_chunk_index ON komite_audit_embeddings(chunk_index);

-- Create vector similarity search index (HNSW for faster similarity search)
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON komite_audit_embeddings 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_conversations_session ON komite_audit_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON komite_audit_conversations(created_at);

CREATE INDEX IF NOT EXISTS idx_agent_logs_conversation ON agent_logs(conversation_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent_name ON agent_logs(agent_name);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for documents table (drop first if exists)
DROP TRIGGER IF EXISTS update_documents_updated_at ON komite_audit_documents;
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON komite_audit_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function for similarity search
CREATE OR REPLACE FUNCTION search_komite_audit_embeddings(
    query_embedding vector(384),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10,
    filter_document_ids uuid[] DEFAULT NULL
)
RETURNS TABLE (
    id uuid,
    document_id uuid,
    content text,
    similarity float,
    chunk_index integer,
    filename varchar,
    category varchar,
    metadata jsonb
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id,
        e.document_id,
        e.content,
        1 - (e.embedding <=> query_embedding) as similarity,
        e.chunk_index,
        d.filename,
        d.category,
        e.metadata
    FROM komite_audit_embeddings e
    JOIN komite_audit_documents d ON e.document_id = d.id
    WHERE 
        1 - (e.embedding <=> query_embedding) > match_threshold
        AND (filter_document_ids IS NULL OR e.document_id = ANY(filter_document_ids))
        AND d.status = 'processed'
    ORDER BY e.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create view for document statistics
CREATE OR REPLACE VIEW document_statistics AS
SELECT 
    d.category,
    COUNT(DISTINCT d.id) as total_documents,
    SUM(d.total_chunks) as total_chunks,
    AVG(d.file_size) as avg_file_size,
    MAX(d.upload_date) as last_upload
FROM komite_audit_documents d
WHERE d.status = 'processed'
GROUP BY d.category;

-- Create view for agent performance
CREATE OR REPLACE VIEW agent_performance AS
SELECT 
    agent_name,
    agent_role,
    COUNT(*) as total_executions,
    AVG(execution_time_ms) as avg_execution_time,
    AVG(tokens_used) as avg_tokens_used,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END)::float / COUNT(*) as success_rate
FROM agent_logs
GROUP BY agent_name, agent_role;

-- Grant necessary permissions (adjust as needed)
-- ALTER TABLE komite_audit_documents ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE komite_audit_embeddings ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE komite_audit_conversations ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE komite_audit_documents IS 'Stores metadata for uploaded documents';
COMMENT ON TABLE komite_audit_embeddings IS 'Stores document chunks and their vector embeddings';
COMMENT ON TABLE komite_audit_conversations IS 'Stores conversation history and query logs';
COMMENT ON TABLE agent_logs IS 'Stores agent execution logs for monitoring';

-- Financial Analyses table - stores AI financial analysis results
CREATE TABLE IF NOT EXISTS financial_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES komite_audit_documents(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    analysis_type VARCHAR(50) DEFAULT 'comprehensive',
    analysis_result JSONB NOT NULL,
    overall_assessment VARCHAR(50),  -- STRONG/MODERATE/WEAK/CRITICAL
    risk_level VARCHAR(50),          -- LOW/MEDIUM/HIGH/CRITICAL
    processing_time_ms INTEGER,
    tokens_used INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for financial analyses
CREATE INDEX IF NOT EXISTS idx_analyses_document_id ON financial_analyses(document_id);
CREATE INDEX IF NOT EXISTS idx_analyses_session_id ON financial_analyses(session_id);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON financial_analyses(created_at);
CREATE INDEX IF NOT EXISTS idx_analyses_assessment ON financial_analyses(overall_assessment);
CREATE INDEX IF NOT EXISTS idx_analyses_risk ON financial_analyses(risk_level);

-- View for analysis statistics
CREATE OR REPLACE VIEW analysis_statistics AS
SELECT
    d.category,
    COUNT(DISTINCT a.id) as total_analyses,
    COUNT(DISTINCT a.document_id) as documents_analyzed,
    AVG(a.processing_time_ms) as avg_processing_time,
    MODE() WITHIN GROUP (ORDER BY a.overall_assessment) as most_common_assessment,
    MODE() WITHIN GROUP (ORDER BY a.risk_level) as most_common_risk_level
FROM financial_analyses a
JOIN komite_audit_documents d ON a.document_id = d.id
GROUP BY d.category;

COMMENT ON TABLE financial_analyses IS 'Stores financial analysis results from AI Senior Financial Analyst';

-- Risk-Audit Mappings table - stores risk-to-audit coverage analysis
CREATE TABLE IF NOT EXISTS risk_audit_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    risk_register_document_id UUID REFERENCES komite_audit_documents(id) ON DELETE CASCADE,
    audit_plan_document_id UUID REFERENCES komite_audit_documents(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    mapping_type VARCHAR(50) DEFAULT 'comprehensive',
    mapping_result JSONB NOT NULL,
    overall_alignment VARCHAR(50),     -- STRONG/MODERATE/WEAK/CRITICAL
    coverage_percentage VARCHAR(10),   -- e.g. "72%"
    critical_gaps_count INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    tokens_used INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for risk_audit_mappings
CREATE INDEX IF NOT EXISTS idx_risk_mappings_risk_doc ON risk_audit_mappings(risk_register_document_id);
CREATE INDEX IF NOT EXISTS idx_risk_mappings_audit_doc ON risk_audit_mappings(audit_plan_document_id);
CREATE INDEX IF NOT EXISTS idx_risk_mappings_session ON risk_audit_mappings(session_id);
CREATE INDEX IF NOT EXISTS idx_risk_mappings_created_at ON risk_audit_mappings(created_at);
CREATE INDEX IF NOT EXISTS idx_risk_mappings_alignment ON risk_audit_mappings(overall_alignment);

-- View for risk mapping statistics
CREATE OR REPLACE VIEW risk_mapping_statistics AS
SELECT
    COUNT(DISTINCT rm.id) as total_mappings,
    COUNT(DISTINCT rm.risk_register_document_id) as unique_risk_registers,
    COUNT(DISTINCT rm.audit_plan_document_id) as unique_audit_plans,
    AVG(rm.processing_time_ms) as avg_processing_time,
    AVG(rm.critical_gaps_count) as avg_critical_gaps,
    MODE() WITHIN GROUP (ORDER BY rm.overall_alignment) as most_common_alignment
FROM risk_audit_mappings rm;

COMMENT ON TABLE risk_audit_mappings IS 'Stores risk-to-audit mapping analysis results from Risk Audit Mapper';

-- Executive Insights table - stores AI executive-level insight analysis results
CREATE TABLE IF NOT EXISTS executive_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES komite_audit_documents(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    analysis_type VARCHAR(50) DEFAULT 'full',
    insight_result JSONB NOT NULL,
    overall_risk_rating VARCHAR(50),    -- LOW/MEDIUM/HIGH/CRITICAL
    attention_required VARCHAR(50),      -- IMMEDIATE/HIGH/MODERATE/MONITOR
    total_exposure_min NUMERIC,
    total_exposure_max NUMERIC,
    management_sentiment VARCHAR(50),    -- PROACTIVE/RESPONSIVE/NEUTRAL/DEFENSIVE/DISMISSIVE
    sentiment_score INTEGER,             -- 1-10
    processing_time_ms INTEGER,
    tokens_used INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for executive_insights
CREATE INDEX IF NOT EXISTS idx_exec_insights_document_id ON executive_insights(document_id);
CREATE INDEX IF NOT EXISTS idx_exec_insights_session_id ON executive_insights(session_id);
CREATE INDEX IF NOT EXISTS idx_exec_insights_created_at ON executive_insights(created_at);
CREATE INDEX IF NOT EXISTS idx_exec_insights_risk_rating ON executive_insights(overall_risk_rating);
CREATE INDEX IF NOT EXISTS idx_exec_insights_attention ON executive_insights(attention_required);
CREATE INDEX IF NOT EXISTS idx_exec_insights_sentiment ON executive_insights(management_sentiment);

-- View for executive insight statistics
CREATE OR REPLACE VIEW executive_insight_statistics AS
SELECT
    d.category,
    COUNT(DISTINCT ei.id) as total_insights,
    COUNT(DISTINCT ei.document_id) as documents_analyzed,
    AVG(ei.processing_time_ms) as avg_processing_time,
    AVG(ei.sentiment_score) as avg_sentiment_score,
    MODE() WITHIN GROUP (ORDER BY ei.overall_risk_rating) as most_common_risk_rating,
    MODE() WITHIN GROUP (ORDER BY ei.management_sentiment) as most_common_sentiment
FROM executive_insights ei
JOIN komite_audit_documents d ON ei.document_id = d.id
GROUP BY d.category;

COMMENT ON TABLE executive_insights IS 'Stores executive-level insight analysis from AI CRO/CFO Advisor';
