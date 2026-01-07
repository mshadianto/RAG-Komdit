"""
Pre-download embedding model during build time
This script is run during Railway build to cache the model
"""
from sentence_transformers import SentenceTransformer

print("Downloading embedding model: sentence-transformers/all-MiniLM-L6-v2")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Model downloaded successfully!")

# Test the model
test_embedding = model.encode("test")
print(f"Model test passed. Embedding dimension: {len(test_embedding)}")
