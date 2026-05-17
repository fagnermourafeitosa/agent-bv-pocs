"""
Provedor de modelo de embeddings.
Isolado aqui para que a troca de modelo não afete o restante do código.
"""
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.rag.config import EMBEDDING_MODEL


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Retorna o modelo de embeddings multilingual configurado."""
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
