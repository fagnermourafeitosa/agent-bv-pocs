"""
Caso de uso: Busca de Contexto Relevante.

Responsabilidade: dada uma pergunta, encontrar os trechos de conhecimento
mais relevantes na base vetorial para embasar uma resposta.
"""
from langchain_core.documents import Document

from app.rag.knowledge_store import connect_to_knowledge_store, as_semantic_retriever


def find_relevant_context(query: str) -> list[Document]:
    """
    Busca os trechos mais relevantes da base de conhecimento para a query.

    Aplica filtro de threshold de similaridade — queries sem correspondência
    semântica retornam lista vazia (sem invenção de contexto).

    Args:
        query: pergunta ou texto de busca do usuário.

    Returns:
        Lista de documentos relevantes, ou lista vazia se não houver match.
    """
    store = connect_to_knowledge_store()
    retriever = as_semantic_retriever(store)
    return retriever.invoke(query)
