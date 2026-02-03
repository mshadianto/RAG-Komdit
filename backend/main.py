"""
FastAPI Backend for RAG Komite Audit System
Provides REST API endpoints for the application
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import uuid
import shutil
from pathlib import Path

from config.config import settings, UPLOAD_DIR
from agents.orchestrator import orchestrator
from agents.financial_analyst import financial_analyst
from agents.risk_audit_mapper import risk_audit_mapper
from agents.executive_insight import executive_insight_analyzer
from backend.document_processor import document_processor
from backend.database import db

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-Agent RAG System for Komite Audit expertise"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    session_id: str
    use_context: bool = True
    max_agents: int = 2

class FeedbackRequest(BaseModel):
    conversation_id: str
    rating: int
    comment: Optional[str] = None

class DocumentDeleteRequest(BaseModel):
    document_id: str

class AnalysisRequest(BaseModel):
    document_id: str
    session_id: Optional[str] = None
    analysis_type: str = "comprehensive"  # comprehensive, quick, ratio_only

class RiskMappingRequest(BaseModel):
    risk_register_document_id: str
    audit_plan_document_id: str
    session_id: Optional[str] = None
    mapping_type: str = "comprehensive"  # comprehensive, quick, gap_only

class ExecutiveInsightRequest(BaseModel):
    document_id: str
    session_id: Optional[str] = None
    analysis_type: str = "full"  # full, quick, risk_focus

class DocumentChatRequest(BaseModel):
    document_id: str
    query: str
    session_id: str

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "llm_model": settings.GROQ_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL
    }

# Query endpoint
@app.post("/query")
async def process_query(request: QueryRequest):
    """
    Process user query through the multi-agent system
    """
    try:
        result = await orchestrator.process_query(
            query=request.query,
            session_id=request.session_id,
            use_context=request.use_context,
            max_agents=request.max_agents
        )
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document upload endpoint
@app.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    category: Optional[str] = Form(None)
):
    """
    Upload and process document
    Processing happens in background
    """
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in document_processor.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported: {list(document_processor.SUPPORTED_FORMATS.keys())}"
            )
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_path)
        
        # Add processing task to background
        background_tasks.add_task(
            document_processor.process_document,
            file_path=str(file_path),
            filename=file.filename,
            file_type=document_processor.SUPPORTED_FORMATS[file_ext],
            file_size=file_size
        )
        
        return {
            "success": True,
            "message": "Document uploaded successfully. Processing in background.",
            "filename": file.filename,
            "file_size": file_size
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List documents endpoint
@app.get("/documents")
async def list_documents(
    category: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100
):
    """List all documents with optional filters"""
    try:
        documents = await db.list_documents(
            category=category,
            status=status,
            limit=limit
        )
        return {"documents": documents}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get document endpoint
@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Get document details by ID"""
    try:
        document = await db.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete document endpoint
@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete document and its embeddings"""
    try:
        success = await db.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "success": True,
            "message": "Document deleted successfully",
            "document_id": document_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Conversation history endpoint
@app.get("/conversations/{session_id}")
async def get_conversation_history(
    session_id: str,
    limit: int = 10
):
    """Get conversation history for a session"""
    try:
        history = await db.get_conversation_history(session_id, limit)
        return {"history": history}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Feedback endpoint
@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for a conversation"""
    try:
        if request.rating < 1 or request.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        success = await db.update_conversation_feedback(
            conversation_id=request.conversation_id,
            rating=request.rating,
            comment=request.comment
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "message": "Feedback submitted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Statistics endpoints
@app.get("/statistics/documents")
async def get_document_statistics():
    """Get document statistics by category"""
    try:
        stats = await db.get_document_statistics()
        return {"statistics": stats}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/statistics/agents")
async def get_agent_statistics():
    """Get agent performance metrics"""
    try:
        stats = await db.get_agent_performance()
        return {"statistics": stats}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agent info endpoint
@app.get("/agents")
async def list_agents():
    """List available expert agents"""
    from config.config import AGENT_ROLES
    return {"agents": AGENT_ROLES}

# Financial Analysis endpoints
@app.post("/analyze")
async def analyze_document(request: AnalysisRequest):
    """
    Analyze a financial document using AI Senior Financial Analyst
    """
    try:
        # Get document metadata
        document = await db.get_document(request.document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        if document.get("status") != "processed":
            raise HTTPException(
                status_code=400,
                detail="Document not yet processed. Please wait for processing to complete."
            )

        # Reconstruct full document text from chunks
        document_text = await db.get_document_full_text(request.document_id)
        if not document_text:
            raise HTTPException(
                status_code=404,
                detail="Document text not found. Document may not have been processed correctly."
            )

        # Run financial analysis
        analysis_result, execution_time, tokens_used = await financial_analyst.analyze_document(
            document_text=document_text,
            document_metadata=document,
            analysis_type=request.analysis_type
        )

        # Save analysis to database
        saved_analysis = await db.create_analysis(
            document_id=request.document_id,
            session_id=request.session_id,
            analysis_type=request.analysis_type,
            analysis_result=analysis_result,
            processing_time_ms=execution_time,
            tokens_used=tokens_used
        )

        return {
            "success": True,
            "document_id": request.document_id,
            "document_name": document.get("filename"),
            "analysis_type": request.analysis_type,
            "analysis": analysis_result,
            "processing_time_ms": execution_time,
            "tokens_used": tokens_used,
            "analysis_id": saved_analysis.get("id") if saved_analysis else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyses")
async def list_analyses(session_id: Optional[str] = None, limit: int = 50):
    """List all analyses with optional session filter"""
    try:
        analyses = await db.list_analyses(session_id, limit)
        return {"analyses": analyses}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyses/{document_id}")
async def get_analyses_by_document(document_id: str, limit: int = 10):
    """Get all analyses for a specific document"""
    try:
        analyses = await db.get_analyses_by_document(document_id, limit)
        return {"analyses": analyses}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Risk-Audit Mapping endpoints
@app.post("/risk-mapping")
async def create_risk_mapping(request: RiskMappingRequest):
    """
    Map risk register against audit plan (PKPT) to identify coverage gaps
    """
    try:
        # Validate risk register document
        risk_doc = await db.get_document(request.risk_register_document_id)
        if not risk_doc:
            raise HTTPException(status_code=404, detail="Risk register document not found")
        if risk_doc.get("status") != "processed":
            raise HTTPException(
                status_code=400,
                detail="Risk register document not yet processed."
            )

        # Validate audit plan document
        audit_doc = await db.get_document(request.audit_plan_document_id)
        if not audit_doc:
            raise HTTPException(status_code=404, detail="Audit plan document not found")
        if audit_doc.get("status") != "processed":
            raise HTTPException(
                status_code=400,
                detail="Audit plan document not yet processed."
            )

        # Get full text for both documents
        risk_text = await db.get_document_full_text(request.risk_register_document_id)
        if not risk_text:
            raise HTTPException(
                status_code=404,
                detail="Risk register text not found."
            )

        audit_text = await db.get_document_full_text(request.audit_plan_document_id)
        if not audit_text:
            raise HTTPException(
                status_code=404,
                detail="Audit plan text not found."
            )

        # Run risk-audit mapping
        mapping_result, execution_time, tokens_used = await risk_audit_mapper.analyze_mapping(
            risk_register_text=risk_text,
            audit_plan_text=audit_text,
            risk_register_metadata=risk_doc,
            audit_plan_metadata=audit_doc,
            mapping_type=request.mapping_type
        )

        # Save to database
        saved_mapping = await db.create_risk_mapping(
            risk_register_document_id=request.risk_register_document_id,
            audit_plan_document_id=request.audit_plan_document_id,
            session_id=request.session_id,
            mapping_type=request.mapping_type,
            mapping_result=mapping_result,
            processing_time_ms=execution_time,
            tokens_used=tokens_used
        )

        return {
            "success": True,
            "risk_register_document_id": request.risk_register_document_id,
            "risk_register_name": risk_doc.get("filename"),
            "audit_plan_document_id": request.audit_plan_document_id,
            "audit_plan_name": audit_doc.get("filename"),
            "mapping_type": request.mapping_type,
            "mapping": mapping_result,
            "processing_time_ms": execution_time,
            "tokens_used": tokens_used,
            "mapping_id": saved_mapping.get("id") if saved_mapping else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk-mappings")
async def list_risk_mappings(session_id: Optional[str] = None, limit: int = 50):
    """List all risk-audit mappings with optional session filter"""
    try:
        mappings = await db.list_risk_mappings(session_id, limit)
        return {"mappings": mappings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk-mappings/{mapping_id}")
async def get_risk_mapping(mapping_id: str):
    """Get a specific risk-audit mapping by ID"""
    try:
        mapping = await db.get_risk_mapping(mapping_id)
        if not mapping:
            raise HTTPException(status_code=404, detail="Risk mapping not found")
        return mapping
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Executive Insight endpoints
@app.post("/executive-insight")
async def create_executive_insight(request: ExecutiveInsightRequest):
    """
    Create executive insight analysis for an audit document
    Extracts: Top 3 Critical Risks, Financial Exposure, Management Sentiment
    """
    try:
        # Validate document exists and is processed
        document = await db.get_document(request.document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        if document.get("status") != "processed":
            raise HTTPException(
                status_code=400,
                detail="Document not yet processed. Please wait for processing to complete."
            )

        # Get full document text
        document_text = await db.get_document_full_text(request.document_id)
        if not document_text:
            raise HTTPException(
                status_code=404,
                detail="Document text not found. Document may not have been processed correctly."
            )

        # Run executive insight analysis
        insight_result, execution_time, tokens_used = await executive_insight_analyzer.analyze_document(
            document_text=document_text,
            document_metadata=document,
            analysis_type=request.analysis_type
        )

        # Save to database
        saved_insight = await db.create_executive_insight(
            document_id=request.document_id,
            session_id=request.session_id,
            analysis_type=request.analysis_type,
            insight_result=insight_result,
            processing_time_ms=execution_time,
            tokens_used=tokens_used
        )

        return {
            "success": True,
            "document_id": request.document_id,
            "document_name": document.get("filename"),
            "analysis_type": request.analysis_type,
            "insight": insight_result,
            "processing_time_ms": execution_time,
            "tokens_used": tokens_used,
            "insight_id": saved_insight.get("id") if saved_insight else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/executive-insights")
async def list_executive_insights(
    session_id: Optional[str] = None,
    risk_rating: Optional[str] = None,
    limit: int = 50
):
    """List all executive insights with optional filters"""
    try:
        insights = await db.list_executive_insights(session_id, risk_rating, limit)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/executive-insights/latest")
async def get_latest_executive_insights(limit: int = 5):
    """Get latest executive insights for dashboard display"""
    try:
        insights = await db.get_latest_executive_insights(limit)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/executive-insights/{insight_id}")
async def get_executive_insight(insight_id: str):
    """Get a specific executive insight by ID"""
    try:
        insight = await db.get_executive_insight(insight_id)
        if not insight:
            raise HTTPException(status_code=404, detail="Executive insight not found")
        return insight
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat-document")
async def chat_with_document(request: DocumentChatRequest):
    """
    Chat with a specific document using RAG
    Filters context to only the specified document
    """
    try:
        # Validate document exists and is processed
        document = await db.get_document(request.document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        if document.get("status") != "processed":
            raise HTTPException(
                status_code=400,
                detail="Document not yet processed."
            )

        # Process query through orchestrator with document filter
        result = await orchestrator.process_query(
            query=request.query,
            session_id=request.session_id,
            use_context=True,
            max_agents=1,
            filter_document_ids=[request.document_id]
        )

        return {
            "success": result.get("success", False),
            "document_id": request.document_id,
            "document_name": document.get("filename"),
            "query": request.query,
            "response": result.get("response"),
            "agents_used": result.get("agents_used", []),
            "context_count": result.get("context_count", 0),
            "processing_time_ms": result.get("processing_time_ms")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
