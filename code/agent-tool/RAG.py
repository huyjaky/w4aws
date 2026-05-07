import uuid
import os
from typing import Any, List
from fastapi import FastAPI, HTTPException, Body
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, SparseVector
from pinecone_text.sparse import BM25Encoder
from openai import OpenAI

qdrant_client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "w4aws"  # Thay bằng tên collection của bạn

openai_client = OpenAI(api_key="asdfasdf", base_url="http://192.168.31.98:8526/v1")  

bm25 = BM25Encoder().default()

app = FastAPI(title="Qdrant Hybrid Upsert API")



def upsert_hybrid_func(text: str, chunk_index: int, cite: str):
    dense_response = openai_client.embeddings.create(
        input=text, model="text-embedding-bge-m3"  # Hoặc text-embedding-ada-002
    )

    dense_vector = dense_response.data[0].embedding

    sparse_result = bm25.encode_documents(text)

    point_id = str(uuid.uuid4())

    point = PointStruct(
        id=point_id,
        vector={
            "w4awsdense": dense_vector,
            "w4awssparse": SparseVector(
                indices=sparse_result["indices"], values=sparse_result["values"]
            ),
        },
        payload={
            "text": text,
            "chunk_index": chunk_index,
            "cite": cite
        },
    )

    # 4. Upsert vào Qdrant
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[point])

    return {
        "point_id": point_id,
        "dense_dim": len(dense_vector),
        "sparse_tokens_count": len(sparse_result["indices"]),
    }

@app.post("/upsert-hybrid")
async def upsert_hybrid(doc: Any = Body(...)):
    results = []
    try:
        for item in doc:
            text = item.get("pageContent")
            chunk_idx = item.get("metadata", {}).get("chunk_index", 0)
            cite = item.get("metadata", {}).get("source_file", 0)

            if not text:
                continue

            res = upsert_hybrid_func(text=text, chunk_index=chunk_idx, cite=cite)
            results.append(res)
            print(f"Upserted: {res}")

        return {"status": "success", "upserted_count": len(results), "details": results}

    except Exception as e:
        print(f"Error during upsert: {e}")
        raise HTTPException(status_code=500, detail=str(e))
