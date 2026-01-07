"""
Embedding Manager for RAG Komite Audit System
Handles text embedding generation using Sentence Transformers
"""
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np
from config.config import settings
import logging

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

class EmbeddingManager:
    """Manages text embeddings using Sentence Transformers"""
    
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.dimension = settings.VECTOR_DIMENSION
        logger.info(f"Embedding model loaded: {settings.EMBEDDING_MODEL}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {str(e)}")
            return 0.0
    
    def chunk_text(
        self,
        text: str,
        chunk_size: int = None,
        chunk_overlap: int = None
    ) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks
        Returns list of dicts with chunk_index, content, and metadata
        """
        chunk_size = chunk_size or settings.CHUNK_SIZE
        chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        # Split by sentences first for better semantic chunks
        sentences = text.replace('\n', ' ').split('. ')
        
        chunks = []
        current_chunk = []
        current_length = 0
        chunk_index = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_length = len(sentence.split())
            
            # If adding this sentence exceeds chunk_size, save current chunk
            if current_length + sentence_length > chunk_size and current_chunk:
                chunk_text = '. '.join(current_chunk) + '.'
                chunks.append({
                    "chunk_index": chunk_index,
                    "content": chunk_text,
                    "metadata": {
                        "word_count": current_length,
                        "sentence_count": len(current_chunk)
                    }
                })
                chunk_index += 1
                
                # Keep last few sentences for overlap
                overlap_sentences = int(len(current_chunk) * (chunk_overlap / chunk_size))
                current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
                current_length = sum(len(s.split()) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add the last chunk
        if current_chunk:
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append({
                "chunk_index": chunk_index,
                "content": chunk_text,
                "metadata": {
                    "word_count": current_length,
                    "sentence_count": len(current_chunk)
                }
            })
        
        logger.info(f"Text split into {len(chunks)} chunks")
        return chunks
    
    def process_document_for_embedding(
        self,
        text: str,
        document_metadata: Dict = None
    ) -> List[Dict[str, Any]]:
        """
        Process a document: chunk it and generate embeddings
        Returns list of dicts with chunk_index, content, embedding, and metadata
        """
        try:
            # Chunk the text
            chunks = self.chunk_text(text)
            
            # Generate embeddings for all chunks
            chunk_texts = [chunk["content"] for chunk in chunks]
            embeddings = self.generate_embeddings_batch(chunk_texts)
            
            # Combine chunks with embeddings
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                processed_chunk = {
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["content"],
                    "embedding": embeddings[i],
                    "metadata": {
                        **chunk["metadata"],
                        **(document_metadata or {})
                    }
                }
                processed_chunks.append(processed_chunk)
            
            logger.info(f"Processed document into {len(processed_chunks)} embedded chunks")
            return processed_chunks
            
        except Exception as e:
            logger.error(f"Error processing document for embedding: {str(e)}")
            raise

# Global embedding manager instance
embedding_manager = EmbeddingManager()
