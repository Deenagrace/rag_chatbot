import json
import hashlib
import numpy as np

def generate_fake_embedding(text, dim=768):
    """Generate a fake but consistent embedding for testing purposes."""
    hash_val = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16)
    np.random.seed(hash_val % (2**32))
    return np.random.rand(dim).tolist()

def prepare_embeddings(text_list):
    """Convert a list of texts to vector format."""
    data = []
    for i, text in enumerate(text_list):
        embedding = generate_fake_embedding(text)
        data.append({
            "id": f"doc-{i}",
            "vector": embedding,
            "metadata": {"text": text}
        })
    return data

if __name__ == "__main__":
    # Example usage
    texts = [
        "What is the admission deadline?",
        "How do I apply for a scholarship?",
        "Where is the library located?"
    ]
    
    output = prepare_embeddings(texts)
    with open("data/embedded_vectors.json", "w") as f:
        json.dump(output, f, indent=2)
    print("✅ Saved embedded_vectors.json with test embeddings.")
