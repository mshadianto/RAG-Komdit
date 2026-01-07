"""
Tests for RAG Komite Audit System
Run with: pytest tests/
"""
import pytest
from backend.embeddings import embedding_manager

def test_embedding_generation():
    """Test embedding generation"""
    text = "Komite Audit bertanggung jawab untuk mengawasi proses audit"
    embedding = embedding_manager.generate_embedding(text)
    
    assert embedding is not None
    assert len(embedding) == 384  # all-MiniLM-L6-v2 dimension
    assert isinstance(embedding, list)

def test_text_chunking():
    """Test text chunking functionality"""
    text = """Komite Audit adalah organ pendukung Dewan Komisaris yang bertugas melakukan 
    pengawasan terhadap pengelolaan perusahaan. Tugas utama Komite Audit meliputi 
    review laporan keuangan, evaluasi audit internal, dan memastikan kepatuhan terhadap 
    peraturan yang berlaku."""
    
    chunks = embedding_manager.chunk_text(text, chunk_size=50, chunk_overlap=10)
    
    assert len(chunks) > 0
    assert all('chunk_index' in chunk for chunk in chunks)
    assert all('content' in chunk for chunk in chunks)

def test_cosine_similarity():
    """Test cosine similarity calculation"""
    text1 = "Audit Committee"
    text2 = "Komite Audit"
    
    emb1 = embedding_manager.generate_embedding(text1)
    emb2 = embedding_manager.generate_embedding(text2)
    
    similarity = embedding_manager.cosine_similarity(emb1, emb2)
    
    assert 0 <= similarity <= 1
    assert similarity > 0.5  # Should be reasonably similar

# Add more tests as needed
