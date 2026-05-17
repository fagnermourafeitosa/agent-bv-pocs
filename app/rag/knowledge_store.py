"""
Fábrica de conexão com o banco vetorial (ChromaDB).
Centraliza a configuração do vector store para que retrieval e ingestion
compartilhem a mesma forma de conexão sem duplicar código.
"""
import chromadb
from langchain_chroma import Chroma

from app.rag.config import (
    CHROMA_HOST,
    CHROMA_PORT,
    KNOWLEDGE_COLLECTION,
    RETRIEVAL_TOP_K,
    RETRIEVAL_SCORE_THRESHOLD,
)
from app.rag.embeddings import get_embedding_model


def connect_to_knowledge_store() -> Chroma:
    """
    Abre conexão com a coleção de conhecimento no ChromaDB.
    Usa distância cosseno, compatível com embeddings semânticos.
    """
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return Chroma(
        client=client,
        collection_name=KNOWLEDGE_COLLECTION,
        embedding_function=get_embedding_model(),
        collection_metadata={"hnsw:space": "cosine"},
    )


def reset_knowledge_store() -> chromadb.HttpClient:
    """
    Remove a coleção existente e retorna o client para recriar.
    Usado durante a re-ingestão para evitar documentos duplicados.
    """
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    try:
        client.delete_collection(KNOWLEDGE_COLLECTION)
    except Exception:
        pass
    return client


def as_semantic_retriever(store: Chroma):
    """
    Cria um retriever com filtro de threshold de similaridade.
    Garante que apenas resultados relevantes sejam retornados.
    """
    return store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": RETRIEVAL_TOP_K,
            "score_threshold": RETRIEVAL_SCORE_THRESHOLD,
        },
    )
