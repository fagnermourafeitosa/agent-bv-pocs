"""Expõe a interface pública do módulo RAG."""
from app.rag.ingestion import ingest_documents
from app.rag.retrieval import find_relevant_context
from app.rag.answering import answer_question

__all__ = ["ingest_documents", "find_relevant_context", "answer_question"]
