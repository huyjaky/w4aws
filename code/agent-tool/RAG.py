from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from pinecone_text.sparse import BM25Encoder
from openai import OpenAI
import cohere  # Thêm thư viện Cohere

qdrant_client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "w4aws"

openai_client = OpenAI(api_key="asdfasdf", base_url="http://192.168.31.98:8526/v1")

# Khởi tạo Cohere Client (Thay API key của bạn vào đây)
cohere_client = cohere.Client("<secret key>")

bm25 = BM25Encoder().default()

app = FastAPI(title="Qdrant Hybrid Search & Cohere Rerank API for n8n")

class SearchQuery(BaseModel):
    query: str
    limit: int = 20           # Số lượng kết quả cuối cùng trả về cho n8n
    retrieve_limit: int = 60  # Số lượng tài liệu lấy từ Qdrant để đem đi rerank (Nên lớn hơn limit)

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

        # 3. Gọi Qdrant Hybrid Search (RRF) - Lấy retrieve_limit thay vì limit
        results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            prefetch=[
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_vector["indices"], values=sparse_vector["values"]
                    ),
                    using="w4awssparse",
                    limit=req.limit*4, 
                ),
                models.Prefetch(
                    query=dense_vector,
                    using="w4awsdense",
                    limit=req.limit*4,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=req.limit*2 
        )

        if not results.points:
            return {"results": []}

        documents_for_rerank = [
            point.payload.get("text", "") for point in results.points
        ]

        rerank_response = cohere_client.rerank(
            model="rerank-english-v3.0", 
            query=req.query,
            documents=documents_for_rerank,
            top_n=req.limit  # Cắt xuống số lượng kết quả cuối cùng yêu cầu
        )

        formatted_results = []
        for rerank_result in rerank_response.results:
            original_point = results.points[rerank_result.index]
            
            formatted_results.append({
                "id": str(original_point.id),
                "rerank_score": rerank_result.relevance_score, # Điểm mới từ Cohere
                "qdrant_rrf_score": original_point.score,      # Điểm RRF cũ từ Qdrant (tham khảo)
                "payload": original_point.payload,
                "cite": original_point.payload.get("text", "")[:200]
            })

        return {"results": formatted_results}

    except Exception as e:
        print(f"Lỗi: {e}")
        raise HTTPException(status_code=500, detail=str(e))
