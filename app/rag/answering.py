"""
Caso de uso: Resposta a Perguntas via RAG.

Responsabilidade: orquestrar a busca de contexto e a geração de resposta
pelo LLM, aplicando as regras de governança comportamental do Banco BV.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.rag.knowledge_store import connect_to_knowledge_store, as_semantic_retriever
from app.rag.config import LLM_MODEL, LLM_TEMPERATURE

load_dotenv()

# ── Prompt com Guardrails Comportamentais ────────────────────────────────────
_SYSTEM_PROMPT = """Você é um assistente virtual do Banco BV, atuando de forma \
"Simples, Parceira, Segura e Inovadora".

REGRAS DE CONDUTA:
1. Baseie sua resposta EXCLUSIVAMENTE no contexto fornecido abaixo.
   Se a resposta não estiver no contexto, responda:
   "Desculpe, não tenho essa informação nas diretrizes do Banco."
2. Nunca prometa taxas ou aprovações sem confirmação sistêmica.
3. Recuse-se, de forma educada, a responder perguntas ofensivas,
   com linguagem inapropriada ou fora do escopo bancário.

Contexto:
{context}

Pergunta:
{question}

Resposta:"""

_PROMPT = PromptTemplate.from_template(_SYSTEM_PROMPT)


def _build_rag_chain():
    """Monta a cadeia RAG: Retriever → Prompt → LLM → Parser."""
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    store = connect_to_knowledge_store()
    retriever = as_semantic_retriever(store)

    def format_context(docs) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | format_context, "question": RunnablePassthrough()}
        | _PROMPT
        | llm
        | StrOutputParser()
    )


def answer_question(question: str) -> str:
    """
    Responde uma pergunta usando o contexto da base de conhecimento (RAG).

    O LLM só utiliza informações presentes nos documentos indexados.
    Perguntas sem contexto relevante ou inapropriadas são recusadas.

    Args:
        question: pergunta do usuário.

    Returns:
        Resposta gerada pelo LLM com base no contexto recuperado.
    """
    chain = _build_rag_chain()
    return chain.invoke(question)
