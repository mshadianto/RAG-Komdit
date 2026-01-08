"""
Database Manager for RAG Komite Audit System
Handles all Supabase database operations
"""
from supabase import create_client, Client
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import logging
from config.config import settings

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations with Supabase"""
    
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )
        logger.info("Database Manager initialized")
    
    # Document Management
    async def create_document(
        self, 
        filename: str,
        file_type: str,
        file_size: int,
        category: str = None,
        tags: List[str] = None,
        metadata: Dict = None
    ) -> Dict:
        """Create a new document entry"""
        try:
            data = {
                "filename": filename,
                "file_type": file_type,
                "file_size": file_size,
                "category": category,
                "tags": tags or [],
                "metadata": metadata or {},
                "status": "uploaded"
            }
            
            response = self.client.table(settings.DOCUMENTS_TABLE).insert(data).execute()
            logger.info(f"Document created: {filename}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            raise
    
    async def update_document_status(
        self,
        document_id: str,
        status: str,
        total_chunks: int = None
    ) -> bool:
        """Update document processing status"""
        try:
            data = {"status": status}
            if total_chunks is not None:
                data["total_chunks"] = total_chunks
                data["processed_date"] = datetime.now().isoformat()
            
            response = self.client.table(settings.DOCUMENTS_TABLE).update(data).eq("id", document_id).execute()
            logger.info(f"Document status updated: {document_id} -> {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating document status: {str(e)}")
            return False
    
    async def get_document(self, document_id: str) -> Optional[Dict]:
        """Get document by ID"""
        try:
            response = self.client.table(settings.DOCUMENTS_TABLE).select("*").eq("id", document_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting document: {str(e)}")
            return None
    
    async def list_documents(
        self,
        category: str = None,
        status: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """List documents with optional filters"""
        try:
            query = self.client.table(settings.DOCUMENTS_TABLE).select("*")
            
            if category:
                query = query.eq("category", category)
            if status:
                query = query.eq("status", status)
            
            response = query.order("upload_date", desc=True).limit(limit).execute()
            return response.data
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return []
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete document and its embeddings"""
        try:
            # Embeddings will be deleted automatically via CASCADE
            response = self.client.table(settings.DOCUMENTS_TABLE).delete().eq("id", document_id).execute()
            logger.info(f"Document deleted: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    # Embedding Management
    async def insert_embeddings(
        self,
        document_id: str,
        chunks: List[Dict[str, Any]]
    ) -> bool:
        """Insert multiple embeddings for a document"""
        try:
            embeddings_data = []
            for chunk in chunks:
                embeddings_data.append({
                    "document_id": document_id,
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["content"],
                    "embedding": chunk["embedding"],
                    "metadata": chunk.get("metadata", {})
                })
            
            # Insert in batches of 100
            batch_size = 100
            for i in range(0, len(embeddings_data), batch_size):
                batch = embeddings_data[i:i + batch_size]
                self.client.table(settings.EMBEDDINGS_TABLE).insert(batch).execute()
            
            logger.info(f"Inserted {len(embeddings_data)} embeddings for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting embeddings: {str(e)}")
            return False
    
    async def similarity_search(
        self,
        query_embedding: List[float],
        match_threshold: float = 0.7,
        match_count: int = 10,
        filter_category: str = None
    ) -> List[Dict]:
        """Perform similarity search using the database function"""
        try:
            # Convert embedding to the format expected by pgvector
            embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
            
            # Call the stored procedure
            response = self.client.rpc(
                "search_komite_audit_embeddings",
                {
                    "query_embedding": embedding_str,
                    "match_threshold": match_threshold,
                    "match_count": match_count
                }
            ).execute()
            
            results = response.data or []
            logger.info(f"Similarity search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []
    
    # Conversation Management
    async def create_conversation(
        self,
        session_id: str,
        user_query: str,
        agent_response: str,
        agents_used: List[str],
        context_documents: List[str] = None,
        similarity_scores: List[float] = None,
        processing_time_ms: int = None
    ) -> Dict:
        """Save conversation to database"""
        try:
            data = {
                "session_id": session_id,
                "user_query": user_query,
                "agent_response": agent_response,
                "agents_used": agents_used,
                "context_documents": context_documents or [],
                "similarity_scores": similarity_scores or [],
                "processing_time_ms": processing_time_ms
            }
            
            response = self.client.table(settings.CONVERSATIONS_TABLE).insert(data).execute()
            logger.info(f"Conversation saved for session: {session_id}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            raise
    
    async def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Get conversation history for a session"""
        try:
            response = self.client.table(settings.CONVERSATIONS_TABLE).select("*").eq("session_id", session_id).order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    async def update_conversation_feedback(
        self,
        conversation_id: str,
        rating: int,
        comment: str = None
    ) -> bool:
        """Update conversation with user feedback"""
        try:
            data = {
                "feedback_rating": rating,
                "feedback_comment": comment
            }
            self.client.table(settings.CONVERSATIONS_TABLE).update(data).eq("id", conversation_id).execute()
            logger.info(f"Feedback updated for conversation: {conversation_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating feedback: {str(e)}")
            return False
    
    # Agent Logging
    async def log_agent_execution(
        self,
        conversation_id: str,
        agent_name: str,
        agent_role: str,
        input_text: str,
        output_text: str,
        execution_time_ms: int,
        tokens_used: int = None,
        status: str = "success",
        error_message: str = None
    ) -> bool:
        """Log agent execution details"""
        try:
            data = {
                "conversation_id": conversation_id,
                "agent_name": agent_name,
                "agent_role": agent_role,
                "input_text": input_text,
                "output_text": output_text,
                "execution_time_ms": execution_time_ms,
                "tokens_used": tokens_used,
                "status": status,
                "error_message": error_message
            }
            
            self.client.table("agent_logs").insert(data).execute()
            return True
            
        except Exception as e:
            logger.error(f"Error logging agent execution: {str(e)}")
            return False
    
    # Statistics and Analytics
    async def get_document_statistics(self) -> List[Dict]:
        """Get document statistics by category"""
        try:
            response = self.client.table("document_statistics").select("*").execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting document statistics: {str(e)}")
            return []
    
    async def get_agent_performance(self) -> List[Dict]:
        """Get agent performance metrics"""
        try:
            response = self.client.table("agent_performance").select("*").execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting agent performance: {str(e)}")
            return []

    # Financial Analysis Methods
    async def get_document_full_text(self, document_id: str) -> Optional[str]:
        """Reconstruct full document text from embeddings chunks"""
        try:
            response = self.client.table(settings.EMBEDDINGS_TABLE)\
                .select("content, chunk_index")\
                .eq("document_id", document_id)\
                .order("chunk_index")\
                .execute()

            if not response.data:
                return None

            # Reconstruct text from ordered chunks
            chunks = sorted(response.data, key=lambda x: x["chunk_index"])
            full_text = "\n\n".join([chunk["content"] for chunk in chunks])

            logger.info(f"Retrieved {len(chunks)} chunks for document {document_id}")
            return full_text

        except Exception as e:
            logger.error(f"Error getting document full text: {str(e)}")
            return None

    async def create_analysis(
        self,
        document_id: str,
        session_id: Optional[str],
        analysis_type: str,
        analysis_result: Dict,
        processing_time_ms: int,
        tokens_used: int = None
    ) -> Optional[Dict]:
        """Save financial analysis to database"""
        try:
            data = {
                "document_id": document_id,
                "session_id": session_id,
                "analysis_type": analysis_type,
                "analysis_result": analysis_result,
                "processing_time_ms": processing_time_ms,
                "tokens_used": tokens_used,
                "overall_assessment": analysis_result.get("executive_summary", {}).get("overall_assessment"),
                "risk_level": analysis_result.get("risk_assessment", {}).get("overall_risk_level")
            }

            response = self.client.table("financial_analyses").insert(data).execute()
            logger.info(f"Analysis saved for document: {document_id}")
            return response.data[0] if response.data else None

        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            return None

    async def get_analyses_by_document(
        self,
        document_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Get analyses for a specific document"""
        try:
            response = self.client.table("financial_analyses")\
                .select("*, komite_audit_documents(filename, category)")\
                .eq("document_id", document_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting analyses: {str(e)}")
            return []

    async def list_analyses(
        self,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """List all analyses with optional session filter"""
        try:
            query = self.client.table("financial_analyses")\
                .select("*, komite_audit_documents(filename, category)")

            if session_id:
                query = query.eq("session_id", session_id)

            response = query.order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error listing analyses: {str(e)}")
            return []

# Global database manager instance
db = DatabaseManager()
