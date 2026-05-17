"""
Configurações centralizadas do módulo RAG.
Toda referência a nomes de modelos, hosts e parâmetros vive aqui.
"""
import os
from pathlib import Path

# ── Diretórios ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs" / "faqs"
FAQ_FILES = ["faq_cartoes.md", "faq_emprestimos.md"]

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
KNOWLEDGE_COLLECTION = "conhecimento_bv"

# ── Embedding ────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "models/gemini-embedding-001"

# ── LLM ─────────────────────────────────────────────────────────────────────
LLM_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
LLM_TEMPERATURE = 0.2

# ── Retrieval ────────────────────────────────────────────────────────────────
RETRIEVAL_TOP_K = 2
RETRIEVAL_SCORE_THRESHOLD = 0.65

# ── Ingestão ─────────────────────────────────────────────────────────────────
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
INGEST_BATCH_SIZE = 5
INGEST_BATCH_DELAY_SECONDS = 2
