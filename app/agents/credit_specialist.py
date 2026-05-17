"""
Nó: Especialista em Crédito

Responsabilidade: responder perguntas sobre limite de crédito, taxas,
empréstimos e financiamentos, usando exclusivamente a base de conhecimento
do Banco BV via RAG.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.state import ConversationState
from app.rag import find_relevant_context

load_dotenv()

_LLM = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    temperature=0.2,
)

_SYSTEM_PROMPT = """Você é o Especialista em Crédito do Banco BV.
Responda APENAS perguntas sobre: limite de crédito, taxas de juros,
financiamento de veículos, empréstimo pessoal e parcelas.

Use EXCLUSIVAMENTE o contexto abaixo para formular sua resposta.
Se o contexto não contiver a informação, diga:
"Não tenho essa informação disponível no momento."

Contexto da base de conhecimento:
{context}"""


def _extract_text(response) -> str:
    content = response.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)


def credit_specialist(state: ConversationState) -> ConversationState:
    question = state["messages"][-1].content
    docs = find_relevant_context(question)
    context = "\n\n".join(d.page_content for d in docs) if docs else "Sem contexto disponível."
    response = _LLM.invoke([
        SystemMessage(content=_SYSTEM_PROMPT.format(context=context)),
        HumanMessage(content=question),
    ])
    chunks_found = len(docs)
    return {
        **state,
        "specialist_answer": _extract_text(response),
        "trace": [
            f"[Especialista em Crédito] Acionado para responder a pergunta.",
            f"[Especialista em Crédito] {chunks_found} trecho(s) relevante(s) recuperado(s) da base vetorial.",
            f"[Especialista em Crédito] Resposta gerada via LLM com contexto RAG.",
        ],
    }
