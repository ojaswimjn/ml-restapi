from sentence_transformers import SentenceTransformer
from typing import List
from pinecone import Pinecone
from db import collection
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key)

index_name = "dev-quickstart-py"
index = pc.Index(index_name)

def chunk_encoding(chunks: List[str], doc_id: str, original_filename: str):
    embeddings = model.encode(chunks, convert_to_numpy=True)
    vectors = []
    metadata_docs = []

    for i, emb in enumerate(embeddings):
        chunk_id = f"{doc_id}-{i}"

        vectors.append({
            "id": chunk_id,
            "values": emb.tolist(),
            "metadata": {
                "text": chunks[i],
                "doc_id": doc_id,               
                "filename": original_filename

            }
        })

        metadata_docs.append({
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "filename": original_filename,
            "text": chunks[i],
        })


    index.upsert(vectors=vectors)

    #mongodb store
    collection.insert_many(metadata_docs)
    
    print(f"Stored {len(vectors)} chunks in Pinecone under doc_id={doc_id}")

    return embeddings
