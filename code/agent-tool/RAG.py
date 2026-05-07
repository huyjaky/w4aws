from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from pinecone_text.sparse import BM25Encoder
from openai import OpenAI

qdrant_client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "w4aws" 

openai_client = OpenAI(api_key="asdfasdf", base_url="http://192.168.31.98:8526/v1")

bm25 = BM25Encoder().default()

app = FastAPI(title="Qdrant Hybrid Search API for n8n")

class SearchQuery(BaseModel):
    query: str
    limit: int = 20

@app.post("/hybrid-search")
def hybrid_search_endpoint(req: SearchQuery):
    try:
        # 1. Sinh Dense Vector
        dense_response = openai_client.embeddings.create(
            input=req.query, model="text-embedding-bge-m3" 
        )
        dense_vector = dense_response.data[0].embedding

        # 2. Sinh Sparse Vector
        sparse_vector = bm25.encode_queries(req.query)

        # 3. Gọi Qdrant Hybrid Search (RRF)
        results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            prefetch=[
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_vector["indices"], values=sparse_vector["values"]
                    ),
                    using="w4awssparse",
                    limit=req.limit * 2, # Lấy dư ra để RRF trộn tốt hơn
                ),
                models.Prefetch(
                    query=dense_vector, 
                    using="w4awsdense",
                    limit=req.limit * 2,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=req.limit
        )

        # 4. Format kết quả trả về dạng JSON thuần để n8n dễ xử lý
        formatted_results = []
        for point in results.points:
            formatted_results.append({
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
                "cite": point.payload.get("text", "")[:200]
            })

        return {"results": formatted_results}

    except Exception as e:
        print(f"Lỗi: {e}")
        raise HTTPException(status_code=500, detail=str(e))
