from sentence_transformers import SentenceTransformer
from typing import List
from pinecone import Pinecone
model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key="pcsk_672f8H_DDCUWftvGkUx8RKa634DmuoRfh3h2oYTqo7BGRt4Cu3ks7HoJscTfLUrLM3VkTJ")
print(pc.list_indexes())  # should print your indexes

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