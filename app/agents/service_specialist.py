"""
Nó: Especialista em Atendimento

Responsabilidade: responder perguntas sobre cartões, conta corrente,
serviços gerais e rotinas do App BV, usando a base de conhecimento via RAG.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.state import ConversationState
from app.rag import find_relevant_context

load_dotenv()

_LLM = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite"),
    temperature=0.2,
)

_SYSTEM_PROMPT = """Você é o Especialista em Atendimento do Banco BV.
Responda APENAS perguntas sobre: cartão de crédito, segunda via, bloqueio,
anuidade, cashback, conta, serviços e dúvidas gerais sobre o App BV.

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


def service_specialist(state: ConversationState) -> ConversationState:
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
            f"[Especialista em Atendimento] Acionado para responder a pergunta.",
            f"[Especialista em Atendimento] {chunks_found} trecho(s) relevante(s) recuperado(s) da base vetorial.",
            f"[Especialista em Atendimento] Resposta gerada via LLM com contexto RAG.",
        ],
    }


def handle_unknown_domain(state: ConversationState) -> ConversationState:
    """Retorna resposta padrão para perguntas fora do escopo."""
    return {
        **state,
        "specialist_answer": (
            "Desculpe, não consigo identificar o assunto da sua pergunta "
            "dentro do escopo do Banco BV. Por favor, reformule ou entre em "
            "contato pelo canal 0800 728 0083."
        ),
        "answer_approved": True,
        "trace": ["[Supervisor] Domínio não reconhecido. Retornando resposta padrão de escopo."],
    }
