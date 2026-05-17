"""
Nó: Supervisor

Responsabilidade:
 1. (Primeira passagem) Interpretar a mensagem do usuário e identificar
    para qual especialista delegar — crédito ou atendimento.
 2. (Segunda passagem, reflexão) Validar a resposta do especialista antes
    de finalizar, garantindo que ela é coerente com a pergunta.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.state import ConversationState

load_dotenv()

_LLM = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    temperature=0,
)

_ROUTING_PROMPT = """Você é o Supervisor de atendimento do Banco BV.
Sua tarefa é ler a mensagem do usuário e identificar o domínio correto:

- Responda APENAS "credito" se a pergunta for sobre: limite de crédito, taxas,
  financiamento, empréstimo, parcelas, juros, aprovação de crédito.
- Responda APENAS "atendimento" se a pergunta for sobre: conta, cartão, segunda via,
  bloqueio, serviços gerais, dúvidas de uso do app, atendimento.
- Responda APENAS "desconhecido" se não se encaixar em nenhum dos dois.

Responda com UMA ÚNICA PALAVRA, sem pontuação."""

_VALIDATION_PROMPT = """Você é o Supervisor de qualidade do Banco BV.
Avalie se a resposta do especialista é adequada para a pergunta do usuário.

Pergunta: {question}
Resposta do especialista: {answer}

Regras:
- Se a resposta for relevante e coerente com a pergunta, responda: APROVADO
- Se a resposta for vaga, incorreta ou fora do escopo, responda: REPROVADO

Responda com UMA ÚNICA PALAVRA."""


def _extract_text(response) -> str:
    """Extrai o texto da resposta do LLM independente do formato."""
    content = response.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)


def supervisor_route(state: ConversationState) -> ConversationState:
    last_message = state["messages"][-1].content
    response = _LLM.invoke([
        SystemMessage(content=_ROUTING_PROMPT),
        HumanMessage(content=last_message),
    ])
    domain = _extract_text(response).strip().lower()
    if domain not in ("credito", "atendimento"):
        domain = "desconhecido"

    label = {"credito": "Crédito", "atendimento": "Atendimento", "desconhecido": "Desconhecido"}
    return {
        **state,
        "domain": domain,
        "trace": [f"[Supervisor] Domínio identificado: {label[domain]}"],
    }


def supervisor_validate(state: ConversationState) -> ConversationState:
    question = state["messages"][-1].content
    answer = state["specialist_answer"]
    prompt = _VALIDATION_PROMPT.format(question=question, answer=answer)
    response = _LLM.invoke([HumanMessage(content=prompt)])
    approved = "aprovado" in _extract_text(response).strip().lower()
    verdict = "APROVADO ✅" if approved else "REPROVADO ⚠️"
    return {
        **state,
        "answer_approved": approved,
        "trace": [f"[Supervisor] Validação da resposta: {verdict}"],
    }
