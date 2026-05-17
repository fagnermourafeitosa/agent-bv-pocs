"""
Router: Base de Conhecimento (RAG)

Endpoints para operar o pipeline RAG:
- Ingestão de documentos na base vetorial
- Busca semântica de contexto
- Resposta a perguntas com guardrails
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag import ingest_documents, find_relevant_context, answer_question

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


class QueryRequest(BaseModel):
    query: str


@router.post("/ingest")
async def ingest():
    """Reindexa os documentos FAQ na base de conhecimento vetorial."""
    try:
        return ingest_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search(request: QueryRequest):
    """Busca os trechos mais relevantes da base para a query informada."""
    try:
        docs = find_relevant_context(request.query)
        return {
            "query": request.query,
            "results": [doc.page_content for doc in docs],
            "total": len(docs),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
async def ask(request: QueryRequest):
    """Responde uma pergunta usando RAG com guardrails comportamentais."""
    try:
        response = answer_question(request.query)
        return {"question": request.query, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
