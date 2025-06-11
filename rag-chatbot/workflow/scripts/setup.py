import pinecone
import json

# ========== CONFIG ==========
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_ENV = "us-east-1"
INDEX_NAME = "n8n-gemini"

# ========== SAMPLE VECTOR DATA ==========
# This assumes you've embedded the documents (e.g., using Gemini inside n8n)
# and you export embeddings like: (id, vector, metadata)

sample_vectors = [
    (
        "doc-1",
        [0.12, 0.53, 0.34, ...],  # ← replace with real embedding
        {"text": "What is the class size at the university?"}
    ),
    (
        "doc-2",
        [0.11, 0.42, 0.95, ...],
        {"text": "What is the application deadline for international students?"}
    )
]

# ========== INIT + UPSERT ==========
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(INDEX_NAME, dimension=768, metric="cosine")  # Gemini vector size ~768, confirm in UI

index = pinecone.Index(INDEX_NAME)
index.upsert(sample_vectors)

print(f"✅ Uploaded {len(sample_vectors)} vectors to Pinecone")
