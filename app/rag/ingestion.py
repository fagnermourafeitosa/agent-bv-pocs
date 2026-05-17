"""
Caso de uso: Ingestão de Documentos na Base de Conhecimento.

Responsabilidade: carregar arquivos de FAQ, dividir em chunks e indexar
no banco vetorial, garantindo idempotência a cada execução.
"""
import time
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.rag.config import (
    DOCS_DIR,
    FAQ_FILES,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    INGEST_BATCH_SIZE,
    INGEST_BATCH_DELAY_SECONDS,
    KNOWLEDGE_COLLECTION,
)
from app.rag.embeddings import get_embedding_model
from app.rag.knowledge_store import reset_knowledge_store


def _load_and_split(file_paths: list[Path]) -> list:
    """Carrega arquivos e divide em chunks para indexação."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = []
    for path in file_paths:
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        docs = TextLoader(str(path), encoding="utf-8").load()
        chunks.extend(splitter.split_documents(docs))
    return chunks


def ingest_documents() -> dict:
    """
    Ingere os documentos de FAQ na base de conhecimento.

    O processo é idempotente: a coleção anterior é removida antes
    de cada ingestão para evitar duplicatas.

    Returns:
        dict com o status e total de chunks indexados.
    """
    file_paths = [DOCS_DIR / filename for filename in FAQ_FILES]
    chunks = _load_and_split(file_paths)

    # Recria a coleção do zero para garantir idempotência
    client = reset_knowledge_store()
    store = Chroma(
        client=client,
        collection_name=KNOWLEDGE_COLLECTION,
        embedding_function=get_embedding_model(),
        collection_metadata={"hnsw:space": "cosine"},
    )

    # Insere em lotes para respeitar rate limits da API de embeddings
    for i in range(0, len(chunks), INGEST_BATCH_SIZE):
        batch = chunks[i : i + INGEST_BATCH_SIZE]
        store.add_documents(documents=batch)
        if i + INGEST_BATCH_SIZE < len(chunks):
            time.sleep(INGEST_BATCH_DELAY_SECONDS)

    return {"status": "success", "indexed_chunks": len(chunks)}
