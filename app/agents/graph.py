"""
Grafo Multiagente — PoC 2: Orquestração com LangGraph

Fluxo:
  [START]
     ↓
  supervisor_route        ← identifica o domínio da pergunta
     ↓ (conditional edge)
  credit_specialist       ← domínio: crédito
  service_specialist      ← domínio: atendimento
  handle_unknown_domain   ← domínio: desconhecido
     ↓
  supervisor_validate     ← loop de reflexão: aprova ou reprova
     ↓
  [END]
"""
from langgraph.graph import StateGraph, START, END

from app.agents.state import ConversationState
from app.agents.supervisor import supervisor_route, supervisor_validate
from app.agents.credit_specialist import credit_specialist
from app.agents.service_specialist import service_specialist, handle_unknown_domain
from app.agents.persona import persona_node
from app.agents.guardrails import guardrail_node


def _route_to_specialist(state: ConversationState) -> str:
    """
    Conditional edge: decide qual nó executar com base no domínio
    identificado pelo Supervisor.
    """
    domain = state.get("domain", "desconhecido")
    routing = {
        "credito": "credit_specialist",
        "atendimento": "service_specialist",
        "desconhecido": "handle_unknown_domain",
    }
    return routing.get(domain, "handle_unknown_domain")


def build_agent_graph() -> StateGraph:
    """
    Constrói e compila o grafo de agentes multiagente do Banco BV.

    Returns:
        Grafo compilado, pronto para invocar com um estado inicial.
    """
    graph = StateGraph(ConversationState)

    # ── Nós ──────────────────────────────────────────────────────────────────
    graph.add_node("supervisor_route", supervisor_route)
    graph.add_node("credit_specialist", credit_specialist)
    graph.add_node("service_specialist", service_specialist)
    graph.add_node("handle_unknown_domain", handle_unknown_domain)
    graph.add_node("persona_node", persona_node)
    graph.add_node("guardrail_node", guardrail_node)
    graph.add_node("supervisor_validate", supervisor_validate)

    # ── Fluxo principal ───────────────────────────────────────────────────────
    graph.add_edge(START, "supervisor_route")

    # Conditional edge: Supervisor roteia para o especialista correto
    graph.add_conditional_edges(
        "supervisor_route",
        _route_to_specialist,
        {
            "credit_specialist": "credit_specialist",
            "service_specialist": "service_specialist",
            "handle_unknown_domain": "handle_unknown_domain",
        },
    )

    # Todos os especialistas convergem para o nó de Persona
    graph.add_edge("credit_specialist", "persona_node")
    graph.add_edge("service_specialist", "persona_node")
    graph.add_edge("handle_unknown_domain", END)

    # Após aplicar persona, passa pelo guardrail ético
    graph.add_edge("persona_node", "guardrail_node")
    graph.add_edge("guardrail_node", "supervisor_validate")

    # Após validação, encerra
    graph.add_edge("supervisor_validate", END)

    return graph.compile()


# Instância singleton do grafo compilado
agent_graph = build_agent_graph()


def run_agent(question: str, session_id: str = None) -> dict:
    """
    Ponto de entrada para executar o grafo multiagente com suporte a observabilidade estendida.

    Args:
        question: Pergunta do usuário.
        session_id: ID da sessão de conversa para agrupar traces relacionados.

    Returns:
        dict com domain, specialist_answer, answer_approved e trace_id.
    """
    from langchain_core.messages import HumanMessage

    import app.langchain_compatibility
    from langfuse.callback import CallbackHandler
    langfuse_handler = CallbackHandler(session_id=session_id)

    initial_state: ConversationState = {
        "messages": [HumanMessage(content=question)],
        "domain": "",
        "specialist_answer": "",
        "answer_approved": False,
        "trace": [f"[Usuário] Pergunta recebida: {question}"],
    }
    result = agent_graph.invoke(initial_state, config={"callbacks": [langfuse_handler]})

    # Registra scores e atualiza o trace no Langfuse
    trace_id = langfuse_handler.get_trace_id()
    if trace_id:
        try:
            # Envia o score de aprovação do supervisor
            langfuse_handler.langfuse.score(
                trace_id=trace_id,
                name="supervisor-approval",
                value=1.0 if result["answer_approved"] else 0.0,
                comment="Aprovação do supervisor no fluxo de governança"
            )
            
            # Detecta se houve violação ética ou injeção detectada no guardrail
            guardrail_violated = any(
                "Violação ética detectada" in str(line) or "Tentativa de Prompt Injection detectada" in str(line)
                for line in result.get("trace", [])
            )
            
            # Envia o score de segurança do guardrail
            langfuse_handler.langfuse.score(
                trace_id=trace_id,
                name="guardrail-safety",
                value=0.0 if guardrail_violated else 1.0,
                comment="Detecção de violação ética no guardrail" if guardrail_violated else "Passou nos guardrails éticos"
            )
            
            # Se foi violado (injection detectado), atualiza as tags e nome do trace
            if guardrail_violated:
                langfuse_handler.langfuse.trace(
                    id=trace_id,
                    name="ethical-guardrail-violation",
                    tags=["guardrail-violation", "prompt-injection-blocked"],
                    public=True
                )
            
            langfuse_handler.flush()
        except Exception:
            # Tolerante a falhas na gravação para não quebrar a execução principal
            pass

    return {
        "domain": result["domain"],
        "answer": result["specialist_answer"],
        "validated": result["answer_approved"],
        "trace": result.get("trace", []),
        "trace_id": trace_id,
    }
