from sentence_transformers import SentenceTransformer
from typing import List
import pinecone

model = SentenceTransformer("all-MiniLM-L6-v2")
pc = pinecone(api_key="pcsk_2jm8Dc_ENksjcQo3t1Fsag9XUG8TWHCZtFSMcJrXjAw4J6HTDmrynTeYKZa67LpCvjQc8D pinecone")

index_name = "dev-quickstart-py"
index = pc.Index(index_name)

def chunk_encoding(chunks: List[str], doc_id: str):
    embeddings = model.encode(chunks, convert_to_numpy=True)

    vectors = []
    for i, emb in enumerate(embeddings):
        vectors.append({
            "id": f"{doc_id}-{i}",
            "values": emb.tolist(),
            "metadata": {
                "text": chunks[i],
                "doc_id": doc_id
            }
        })

    index.upsert(vectors=vectors)
    print(f"Stored {len(vectors)} chunks in Pinecone under doc_id={doc_id}")

    return embeddings