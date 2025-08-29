from sentence_transformers import SentenceTransformer
from typing import List

def chunk_encoding(chunks: List[str]) -> list:

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings
